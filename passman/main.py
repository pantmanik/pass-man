import config
import os.path
from passman.Manager.UserDataManager import get_data_manager


def init():
    # config.init_config()
    # print(f'Work dir : {config.WORK_DIR}')
    data_manager = get_data_manager()


def main():
    init()


if __name__ == '__main__':
    main()
