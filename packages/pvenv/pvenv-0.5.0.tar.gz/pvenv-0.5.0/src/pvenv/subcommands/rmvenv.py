import shutil
from argparse import Namespace
from pathlib import Path
from typing import List

from pvenv.subcommands.base import BaseCommand


class Command(BaseCommand):
    def __init__(self, options: Namespace):
        super().__init__(options)
        self.base_dir: Path = options.base_dir
        self.venv_to_remove: List[str] = options.venvs_to_remove

    def run(self):
        for venv in self.venv_to_remove:
            venv_path = self.base_dir.joinpath(venv)
            if not venv_path.exists():
                print(f"{venv} does not exist, skipping...")
                continue
            try:
                shutil.rmtree(venv_path)
            except (PermissionError, NotADirectoryError):
                print(f"Cannot delete {venv}, skipping...")
                continue

            print(f"{venv} removed successfully!")
