import os
from argparse import Namespace
from pathlib import Path

from pvenv.subcommands.base import BaseCommand


class Command(BaseCommand):
    def __init__(self, options: Namespace):
        super().__init__(options)
        self.base_dir: Path = options.base_dir
        self.venv: str = options.venv
        self.cd: bool = options.cd

    def run(self):
        venv_path = self.base_dir.joinpath(self.venv)
        if not venv_path.exists():
            raise RuntimeError(f"Venv {self.venv} doesn't exist, aborting...")

        if os.getenv("VIRTUAL_ENV"):
            print("dvenv")

        project = venv_path.joinpath(".project")
        if project.exists():
            if self.cd:
                with open(project) as file:
                    print(f"cd {file.read().strip()}")
            environment = venv_path.joinpath(".environment")
            if environment.exists():
                with open(environment) as file:
                    for line in file:
                        print(f"invenv {line.strip()}")

        activate = venv_path.joinpath("bin/activate")
        if activate.exists():
            print(f". {activate}")
        else:
            print(f"export VIRTUAL_ENV=dummy_{self.venv}")
