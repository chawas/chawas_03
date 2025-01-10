import os
import json

#from src.config3 import IMAGES_DIR

#from src.services.download_satellite_imgs6 import SRC_DIR

# Load the configuration JSON
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
#IMAGES_DIR = os.path.join(BASE_DIR, "", "config.json")
CONFIG_PATH = os.path.join(BASE_DIR, "src", "config.json")
SRC_DIR = os.path.join(BASE_DIR, "src")
with open(CONFIG_PATH, "r") as config_file:
    CONFIG = json.load(config_file)

# Extract paths and settings from CONFIG
VENV_ACTIVATE = os.path.join(BASE_DIR, CONFIG["paths"]["venv_activate"])
LOGS_DIR = os.path.join(BASE_DIR, CONFIG["paths"]["logs"])
CHROMEDRIVER_PATH = CONFIG["chromedriver"]["path"]
IMAGES_DIR = os.path.join(BASE_DIR, CONFIG["paths"]["images_dir"])

BASE_DIR = CONFIG.get("base_dir", os.getcwd())  # Default to the current working directory
WX_PRESENTATION_IMAGES = os.path.join(BASE_DIR, CONFIG["paths"]["wx_presentation_images"])
URL_LIST = CONFIG["url_list"]
# Retry configuration
MAX_RETRIES = CONFIG["retry_config"]["max_retries"]
DELAY_SECONDS = CONFIG["retry_config"]["delay_seconds"]

# Debugging
if __name__ == "__main__":
    print("BASE_DIR:", BASE_DIR)
    print("SRC_DIR:", SRC_DIR)
    print("IMAGES_DIR:", IMAGES_DIR)
    print("LOGS_DIR:", LOGS_DIR)
    print("CONFIG_PATH:", CONFIG_PATH)
    print("VENV_ACTIVATE:", VENV_ACTIVATE)
    print("CHROMEDRIVER_PATH:", CHROMEDRIVER_PATH)
    print("MAX_RETRIES:", MAX_RETRIES)
    print("DELAY_SECONDS:", DELAY_SECONDS)
