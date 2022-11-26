# from tpot import TPOTRegressor, decorators
from Utility import Utility_base
from pprint import pprint
from typing import Any, Dict

my_utils = Utility_base.Utils()


class WrapperMain:

    __slots__ = (
        'tpot_regressor_config'
    )

    def __init__(self):
        self.tpot_regressor_config: Dict[Any, Any] = my_utils.config['AUTOML_CONFIGURATIONS']

    def chill(self):
        pass

    def process(self):
        pass


if __name__ == '__main__':
    wm = WrapperMain()
    pprint(wm.tpot_regressor_config)
