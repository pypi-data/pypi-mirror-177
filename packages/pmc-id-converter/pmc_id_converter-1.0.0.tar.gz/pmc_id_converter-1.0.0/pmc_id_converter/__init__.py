import json
from pathlib import Path

from pmc_id_converter.core import API


BASE_DIR = Path(__file__).resolve().parent

version_info = json.load(BASE_DIR.joinpath('version.json').open())
__version__ = version_info['version']
