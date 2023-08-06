import os
from argparse import Namespace
from typing import List

from pvenv.subcommands.base import BaseCommand


class Command(BaseCommand):
    def __init__(self, options: Namespace):
        super().__init__(options)
        self.env_vars: List[str] = options.env_vars
        self.files = options.files

    @staticmethod
    def parse_env_var(line: str) -> List[str]:
        return line.split("=", maxsplit=1)

    def run(self):
        new_vars = {}
        for file in self.files:
            with open(file) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        key, value = self.parse_env_var(line)
                        new_vars[key] = value
        for env_var in self.env_vars:
            key, value = self.parse_env_var(env_var)
            new_vars[key] = value

        if new_vars:
            if self._prefix in os.environ:
                raise RuntimeError("Already in a venv, aborting...")
            print(f"export {self._prefix}=true")
        for key, value in new_vars.items():
            print(f"export {self._prefix}_{key}={os.getenv(key, '')}")
            print(f"export {key}={value}")
