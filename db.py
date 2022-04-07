import os
import dataset
from dotenv import load_dotenv

load_dotenv()

TEMP_PATH = os.environ.get("TEMP_PATH")
DB_NAME = os.environ.get("DB_NAME")

db_path = os.path.join(os.path.dirname(__file__), TEMP_PATH)
if not os.path.isdir(db_path):
    os.mkdir(db_path)

db = dataset.connect(f"sqlite:///{db_path}/{DB_NAME}.db")