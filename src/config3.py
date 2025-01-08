import os
import json

# Get the directory of the current script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)  # One directory up
print("base dir : BASE_DIR")
# Load configuration from config.json
def load_config():
    config_path = os.path.join(BASE_DIR, "config3.json")
    with open(config_path, "r") as config_file:
        return json.load(config_file)

CONFIG = load_config()

# Convenience variables
LOG_DIR = os.path.join(BASE_DIR, CONFIG["paths"]["logs"])
IMAGES_DIR = os.path.join(BASE_DIR, CONFIG["paths"]["images_dir"])
OUTPUT_DIR = os.path.join(BASE_DIR, CONFIG["paths"]["output_dir"])
VENV_ACTIVATE = os.path.join(BASE_DIR, CONFIG["paths"]["venv_activate"])
CHROMEDRIVER_PATH = CONFIG["chromedriver"]["path"]

# Retry configuration
MAX_RETRIES = CONFIG["retry_config"]["max_retries"]
DELAY_SECONDS = CONFIG["retry_config"]["delay_seconds"]
