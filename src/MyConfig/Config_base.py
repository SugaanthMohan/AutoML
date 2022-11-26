from pathlib import Path
import os
import pprint
from configparser import ConfigParser
from ast import literal_eval
from datetime import datetime
import tempfile
from typing import Any, Dict, List


class Configuration:
    __slots__ = (
        '__file',
        '__directory',
        'configuration'
    )

    def __init__(self):
        self.__file: str = "AutoML.ini"
        self.__directory: str = "MyConfig"
        self.configuration: Dict[Any, Any] = self.load_configuration()

    def get_configuration_file(self) -> str:

        return str(
            os.path.join(
                Path(__file__).parent.parent,
                self.__directory,
                self.__file
            )
        )

    def load_all_configs(self, config_file_: str) -> Dict[Any, Any]:

        # DEFINE CONFIGURATION
        configuration = dict()

        # CREATE CONFIG OBJECT
        cfg_obj = ConfigParser()

        cfg_obj.read(
            filenames=config_file_,
            encoding='utf-8'
        )

        for section in cfg_obj.sections():
            configuration[section] = dict(cfg_obj[section])

        return configuration

    def load_configuration(self) -> Dict[Any, Any]:

        config_file = self.get_configuration_file()

        config = self.load_all_configs(config_file_=config_file)

        config = self.post_process_configs(config=config)

        return config

    def automl_base_config_updates(self, prefix: str, config: Dict[Any, Any]) -> Dict[Any, Any]:

        config[prefix]['models'] = list(
            map(
                str,
                config[prefix]['models'].split('\n')
            )
        )

        return config

    def parse_model(self, model_configuration: Dict[Any, Any]):

        for key in model_configuration.keys():
            model_configuration[key] = literal_eval(model_configuration[key])

        return model_configuration

    def parse_and_load_models(self, model_list: List[Any], config: Dict[Any, Any]) -> Dict[Any, Any]:

        regressor_models_dict = {}

        for model_name in model_list:
            model_config = self.parse_model(model_configuration=config[model_name])

            regressor_models_dict.update({model_name: model_config})

            config.pop(model_name)

        return regressor_models_dict

    def automl_regressor_config_updates(self, prefix: str, config: Dict[Any, Any]) -> Dict[Any, Any]:

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

        config[prefix]['config_dict'] = self.parse_and_load_models(
            model_list=config["AUTOML"]['models'],
            config=config
        )

        config.pop('AUTOML')

        return config

    def logger_config_update(self, config: Dict[Any, Any]) -> Dict[Any, Any]:

        timer = datetime.now().strftime("%Y%m%d_%H%M%S")

        log_file = config['LOGGER']['prefix'].replace('(?Timestamp)', timer)

        if config['LOGGER']['type'] == 'TEMP':
            logger_dir = os.path.join(
                tempfile.gettempdir(),
                config['LOGGER']['dir']
            )

        elif config['LOGGER']['type'] == 'FILESYSTEM':
            logger_dir = config['LOGGER']['dir']
        else:
            raise IsADirectoryError("UNABLE TO FIND TEMP DIRECTORY TYPE")

        Path(logger_dir).mkdir(parents=True, exist_ok=True)

        config['LOG_FILE'] = os.path.join(logger_dir, log_file)

        config.pop('LOGGER')

        return config

    def post_process_configs(self, config: Dict[Any, Any]) -> Dict[Any, Any]:

        config = self.automl_base_config_updates(prefix="AUTOML", config=config)

        config = self.automl_regressor_config_updates(
            prefix=config['AUTOML']['configuration'], config=config
        )

        config = self.logger_config_update(config=config)

        # DROP UNNECESSARY FEATURES

        return config


if __name__ == '__main__':
    cfg = Configuration()
    pprint.pprint(cfg.configuration)
