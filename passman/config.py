import os.path
import yaml

WORK_DIR = None
CONFIG_PATH = 'settings.yaml'
SINGLETON_OBJECT = None

class Config:
    work_dir = None

    def __init__(self):
        if not os.path.exists(CONFIG_PATH):
            print('Cannot find settings.yaml. Please make one in the passman directory!')
            return
        config = None
        with open(CONFIG_PATH, 'r') as config_file:
            config = yaml.safe_load(config_file)
        if config is None:
            print('Could not open config file!')
            return
        self.work_dir = config.get('work-directory')

def get_config():
    global SINGLETON_OBJECT
    if SINGLETON_OBJECT is None:
        print('Initializing Config.')
        SINGLETON_OBJECT = Config()
    return SINGLETON_OBJECT


def init_config():
    global WORK_DIR
    if not os.path.exists(CONFIG_PATH):
        print('Cannot find settings.yaml. Please make one in the passman directory!')
        return False
    config = None
    with open(CONFIG_PATH, 'r') as config_file:
        config = yaml.safe_load(config_file)
    if config is None:
        print('Could not open config file!')
        return False
    WORK_DIR = config.get('work-directory')

# init_config()
