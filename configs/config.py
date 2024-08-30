import pathlib

import yaml

CONFIG = None

config_path = pathlib.Path("./config.yaml").absolute()
with open(config_path) as config_file:
    CONFIG = yaml.safe_load(config_file)
