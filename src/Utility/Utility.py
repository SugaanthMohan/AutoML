from Utility.Config import Configuration
from pprint import pprint


class Utils:
    # ABSTRACT AND USAGE CLASS
    __slots__ = (
        'config'
    )

    def __init__(self):
        self.config: Configuration = Configuration().configuration


if __name__ == '__main__':
    uo = Utils()
    pprint(uo.config)