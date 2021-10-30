import json
import os

INITIAL_EXTENSIONS = [
    'Cogs.botstuff',
    'Cogs.owner',
    'Cogs.errorhandler',
    'jishaku'
]

os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"