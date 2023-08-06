import os
from argparse import Namespace
from pathlib import Path
from typing import List

from pvenv.subcommands.base import BaseCommand

DEV_NULL = Path(os.devnull)


class Command(BaseCommand):
    def __init__(self, options: Namespace):
        super().__init__(options)
        self.base_dir: Path = options.base_dir
        self.venv: str = options.venv
        self.python: str = options.python
        self.project: Path = Path(options.project).absolute()
        self.environments: List[Path] = self._get_environments()

    def _get_project(self) -> Path:
        project = self._options.project
        return Path(project).absolute() if project else DEV_NULL

    def _get_environments(self) -> List[Path]:
        environments = self._options.environments
        if self.project == DEV_NULL and environments:
            raise RuntimeError("Cannot set environ in independent")
        return [self.project.joinpath(environ) for environ in environments]

    def run(self):
        venv_path = self.base_dir.joinpath(self.venv)
        if venv_path.exists():
            raise RuntimeError(f"Venv {self.venv} already exists, aborting...")

        if self.python == "current":
            print(f"python -m venv {venv_path}")
        elif self.python:
            print(f"pyenv shell {self.python}")
            print(f"python -m venv {venv_path}")
        else:
            print(f"mkdir -p {venv_path}")

        if self.project != DEV_NULL:
            print(f"echo {self.project} > {venv_path}/.project")

        for i, environment in enumerate(self.environments):
            if i == 0:
                print(f": > {venv_path}/.environment")
            print(f"cat {environment} >> {venv_path}/.environment")

        print(f"avenv {self.venv}")

        if self.python:
            print("pip install --upgrade pip wheel")
