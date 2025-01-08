import os
import environ
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

def return_env_value(key: str) -> str:
	env = environ.Env()
	environ.Env.read_env(
	    env_file=os.path.join(BASE_DIR, '.env')
	)


	return env(key)

