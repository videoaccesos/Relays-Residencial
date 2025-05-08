import os, yaml
CONFIG_PATH = os.getenv('FLASK_CONFIG', 'config.yaml')
with open(CONFIG_PATH) as f:
    CONFIG = yaml.safe_load(f)