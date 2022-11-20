from tpot import TPOTRegressor, decorators
from Utility.Utility import Utils

my_utils = Utils()

class WrapperMain:

    __slots__ = (
        'tpot_regressor_config'
    )

    def __init__(self):
        self.tpot_regressor_config: dict = my_utils.config['AUTOML_CONFIGURATIONS']

    def chill(self):
        pass

    def process(self):
        pass


if __name__ == '__main__':
    wm = WrapperMain()
    print(wm.regressor_config)
    print(wm.tpot_regressor_config)
