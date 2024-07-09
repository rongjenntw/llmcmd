import json, os

DEBUG = 4
INFO = 3
WARN = 2
ERROR = 1
FATAL = 0
LEVELS = {0:"FATAL: ",1:"ERROR: ",2:"WARN: ",3:"INFO: ",4:"DEBUG: "}

with open(os.getenv('LLMCMD_CONFIG_FILE_PATH') or 'config.json') as config_file:
    config = json.load(config_file)
    LOG_LEVEL = config.get('log_level')
def stdout(msg, level=DEBUG):
    if level <= LOG_LEVEL:
        print(LEVELS[level] + str(msg))