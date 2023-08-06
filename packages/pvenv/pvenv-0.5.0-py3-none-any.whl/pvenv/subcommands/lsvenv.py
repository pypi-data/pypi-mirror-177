from argparse import Namespace
from pathlib import Path

from pvenv.subcommands.base import BaseCommand


class Command(BaseCommand):
    def __init__(self, options: Namespace):
        super().__init__(options)
        self.base_dir: Path = options.base_dir

    def run(self):
        for directory in sorted(self.base_dir.glob("*")):
            if directory.is_dir():
                print(directory.name)
