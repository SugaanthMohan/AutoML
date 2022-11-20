from pathlib import Path
import os, pprint
from configparser import ConfigParser
from ast import literal_eval
from datetime import datetime
import tempfile

class Configuration:

    __slots__ = (
        '__file',
        '__directory',
        'configuration'
    )

    def __init__(self):
        self.__file: str = "AutoML.ini"
        self.__directory: str = "Config"
        self.configuration: dict = self.load_configuration()

    def get_configuration_file(self) -> str:

        return str(
            os.path.join(
                Path(__file__).parent.parent,
                self.__directory,
                self.__file
            )
        )

    def load_all_configs(self, config_file_: str) -> dict:

        # DEFINE CONFIGURATION
        configuration = dict()

        # CREATE CONFIG OBJECT
        cfg_obj = ConfigParser()

        # SET STRING CONFIGURATION
        cfg_obj.optionxform = str

        cfg_obj.read(
            filenames=config_file_,
            encoding='utf-8'
        )

        for section in cfg_obj.sections():
            configuration[section] = dict(cfg_obj[section])

        return configuration

    def load_configuration(self) -> dict:

        config_file = self.get_configuration_file()

        config = self.load_all_configs(config_file_=config_file)

        config = self.post_process_configs(config=config)

        return config

    def automl_base_config_updates(self, prefix: str, config: dict) -> dict:

        config[prefix]['MODELS'] = list(
            map(
                str,
                config[prefix]['MODELS'].split('\n')
            )
        )

        return config

    def parse_model(self, model_configuration: dict):

        for key in model_configuration.keys():

            model_configuration[key] = literal_eval(model_configuration[key])

        return model_configuration

    def parse_and_load_models(self, model_list: list, config: dict) -> dict:

        regressor_models_dict = {}

        for model_name in model_list:

            model_config = self.parse_model(model_configuration=config[model_name])

            regressor_models_dict.update({model_name: model_config})

            config.pop(model_name)

        return regressor_models_dict

    def automl_regressor_config_updates(self, prefix: str, config: dict) -> dict:

        config[prefix]['generations'] = int(
            config[prefix]['generations']
        )

        config[prefix]['population_size'] = int(
            config[prefix]['population_size']
        )

        config[prefix]['verbosity'] = int(
            config[prefix]['verbosity']
        )

        config[prefix]['use_dask'] = bool(int(
            config[prefix]['use_dask']
        ))

        config[prefix]['warm_start'] = bool(int(
            config[prefix]['warm_start']
        ))

        config[prefix]['n_jobs'] = int(
            config[prefix]['n_jobs']
        )

        config['REGRESSOR_CONFIG'] = self.parse_and_load_models(
            model_list=config["AUTOML"]['MODELS'],
            config=config
        )

        config.pop(prefix)
        config.pop('AUTOML')

        return config

    def logger_config_update(self, config: dict) -> dict:

        timer = datetime.now().strftime("%Y%m%d_%H%M%S")

        log_file = config['LOGGER']['PREFIX'].replace('(?Timestamp)', timer)

        if config['LOGGER']['TYPE'] == 'TEMP':
            logger_dir = os.path.join(
                tempfile.gettempdir(),
                config['LOGGER']['DIR']
            )

        elif config['LOGGER']['TYPE'] == 'FILESYSTEM':
            logger_dir = config['LOGGER']['DIR']
        else:
            raise IsADirectoryError("UNABLE TO FIND TEMP DIRECTORY TYPE")

        Path(logger_dir).mkdir(parents=True, exist_ok=True)

        config['LOG_FILE'] = os.path.join(logger_dir, log_file)

        config.pop('LOGGER')

        return config

    def post_process_configs(self, config: dict) -> dict:

        config = self.automl_base_config_updates(prefix="AUTOML", config=config)

        config = self.automl_regressor_config_updates(
            prefix=config['AUTOML']['CONFIGURATION'], config=config
        )

        config = self.logger_config_update(config=config)

        # DROP UNNECESSARY FEATURES

        return config


if __name__ == '__main__':
    cfg = Configuration()
    pprint.pprint(cfg.configuration)
