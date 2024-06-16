from config_manager import initialize_config
from gui import create_main_window
from logging_setup import *


def main():
    _ = initialize_config()
    create_main_window()


if __name__ == "__main__":
    main()
