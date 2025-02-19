from pathlib import Path
from os import getenv
import yaml


def config():
    root_dir = Path(__file__).parent
    with open(f"{root_dir}/config/project.yml", 'r', encoding='utf-8') as file:
        return yaml.load(file.read(), Loader=yaml.BaseLoader)['environment'][getenv('STAGE')]
