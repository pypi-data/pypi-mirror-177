import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Match

from cleo.application import Application
from cleo.commands.command import Command
from cleo.helpers import argument, option
from poetry.plugins.application_plugin import ApplicationPlugin


class TemplateCommand(Command):

    target_dir: Path
    source_files: List[Path]
    lock: Dict[str, Any]

    def c_ignore(self, src: str) -> None:
        source_files = self.source_files[:]
        for exclude in Path(".").glob(str(src)):
            if exclude.is_dir():
                source_files = [p for p in source_files if not p.is_relative_to(exclude)]
            elif exclude in source_files:
                source_files.remove(exclude)
        self.source_files = source_files

    def c_ask(self, question: str, default: Any = None) -> Any:
        if question in self.lock["questions"]:
            return self.lock["questions"][question]
        answer = self.lock["questions"][question] = self.ask(question, default)
        return answer

    def handle(self) -> None:
        self.init()
        self.io.write_line(f"<info>Clone {self.lock['repository']}</>")
        tmp_dir = tempfile.mkdtemp()
        try:
            subprocess.check_output(
                ["git", "clone", "--depth=1", f"ssh://{self.lock['repository']}", tmp_dir],
                stderr=subprocess.DEVNULL,
            )
            self.enroll(tmp_dir)
        finally:
            shutil.rmtree(tmp_dir)

    def init(self) -> None:
        raise NotImplementedError()

    def enroll(self, source_dir: str) -> None:
        os.chdir(source_dir)
        if not Path("pytemplate.py").exists():
            raise RuntimeError("Script pytemplate.py does not exist.")
        self.source_files = [p for p in Path(".").glob("**/*") if not p.is_relative_to(".git")]
        self.c_ignore("pytemplate.py")
        code_globals = {
            "ignore": self.c_ignore,
            "ask": self.c_ask,
            "__builtins__": {},
        }
        code_locals = {**self.lock["context"]}
        exec(Path("pytemplate.py").read_text(encoding="utf-8"), code_globals, code_locals)
        new_files = {}
        for p in self.source_files:
            if p.is_dir():
                continue
            if p.name.startswith("@"):
                data = self.apply_context(p.read_text(encoding="utf-8"), code_locals).encode(
                    "utf-8"
                )
            else:
                data = p.read_bytes()
            source_hash = hashlib.md5(data).hexdigest()
            t = (p.parent / p.name[1:]) if (p.name.startswith("@") or p.name.startswith("#")) else p
            new_files[str(t)] = source_hash
            if (self.target_dir / t).exists():
                target_hash = hashlib.md5((self.target_dir / t).read_bytes()).hexdigest()
                if self.lock["files"].get(str(t)) != target_hash:
                    self.io.write_line(f". <c2>skip</c2> <c1>{t}</c1>")
                    continue
            if self.lock["files"].get(str(t)) != source_hash:
                self.io.write_line(f". <c2>write</c2> <c1>{t}</c1>")
                if not (self.target_dir / t).parent.exists():
                    os.makedirs((self.target_dir / t).parent)
                (self.target_dir / t).write_bytes(data)
        os.chdir(self.target_dir)
        self.lock["files"] = new_files
        Path("pytemplate.lock").write_bytes(json.dumps(self.lock, indent=2).encode("utf-8"))
        self.done()
        self.line("\n✨ Done!")

    def apply_context(self, content: str, context: Dict[str, Any]) -> str:
        def repl(m: Match) -> str:
            val = repr(context.get(m.group(1), ""))
            return (
                val[1:-1].replace('"', '\\"')
                if val.startswith("'")
                else val[1:-1].replace("'", "\\'")
            )

        return re.sub(r"{%\s*([a-zA-Z_0-9]+)\s*%}", repl, content)

    def done(self) -> None:
        self.call("update")


class TemplateInitCommand(TemplateCommand):

    name = "template init"
    description = "Create project from template."
    arguments = [
        argument("repository", "Template repository.", multiple=False),
        argument("target", "Target directory name.", multiple=False),
    ]

    def init(self):
        self.target_dir = Path(os.getcwd()) / self.argument("target")
        self.lock = {
            "files": {},
            "repository": self.argument("repository"),
            "context": {"target": self.argument("target")},
            "questions": {},
        }
        if self.target_dir.exists() and not self.target_dir.is_dir():
            raise RuntimeError(f"File {self.target_dir} exists.")
        if self.target_dir.exists() and any(
            1 for p in self.target_dir.glob("**/*") if not p.is_relative_to(".git")
        ):
            raise RuntimeError(f"Target directory {self.target_dir} is not empty.")


class TemplateUpdateCommand(TemplateCommand):
    name = "template update"
    description = "Update project from template."
    arguments = []
    options = [
        option("update", description="Run poetry update."),
    ]

    def init(self):
        self.target_dir = Path(os.getcwd())
        if not Path("pytemplate.lock").exists():
            raise RuntimeError("Missing pytemplate.lock file.")
        self.lock = json.loads(Path("pytemplate.lock").read_text(encoding="utf-8"))

    def done(self):
        if self.option("update"):
            self.call("update")


class TemplatePlugin(ApplicationPlugin):
    def activate(self, application: Application, *args: Any, **kwargs: Any) -> None:
        application.command_loader.register_factory("template init", TemplateInitCommand)
        application.command_loader.register_factory("template update", TemplateUpdateCommand)
