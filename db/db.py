import os

import dataset

from configs.config import CONFIG


class LocalDatabase:
    def __init__(self, temp_path: str, name: str):
        db_path = os.path.join(os.path.dirname(__file__), temp_path)
        if not os.path.isdir(db_path):
            os.mkdir(db_path)
        self.DB = dataset.connect(f"sqlite:///{db_path}/{name}.db")


LOCAL_DATABASE = LocalDatabase(temp_path=CONFIG.get("TEMP_PATH"), name=CONFIG.get("DB_NAME")).DB
