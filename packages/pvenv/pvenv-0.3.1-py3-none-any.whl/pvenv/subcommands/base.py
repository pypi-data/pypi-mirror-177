from argparse import Namespace


class BaseCommand:
    def __init__(self, options: Namespace):
        self._prefix = "_pvenv_env"
        self._options = options

    def run(self):
        raise NotImplementedError(f"{self.__class__.__name__} must implement run")
