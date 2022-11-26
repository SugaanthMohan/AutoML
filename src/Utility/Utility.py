from src.Utility.Config import Configuration
from pprint import pprint
from typing import Any, Dict


class Utils:
    # ABSTRACT AND USAGE CLASS
    __slots__ = (
        'config'
    )

    def __init__(self):
        self.config: Dict[Any, Any] = Configuration().configuration


if __name__ == '__main__':
    uo = Utils()
    pprint(uo.config)
