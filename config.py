"""
Handle reading of the config file, which on POSIX-compliant systems will be
created in ~/.config/assignment-list-pyqt5/config.py
"""

import configparser
import os
import sys

Globals = __import__("globals")

class Config():
    def __init__(self):
        self.config_path = os.path.join(
            os.path.expanduser("~"),
            ".config",
            "assignment-list-pyqt5",
            "config")

        if not os.path.exists(self.config_path):
            self.createConfig()

        self.loadConfig()

    def loadConfig(self):
        config = configparser.ConfigParser()

        try:
            config.read(self.config_path)
        except:
            print("Could not parse config file '{}'".format(self.config_path))
        
        if "paths" in config:
            if config["paths"]["db_path"]:
                Globals.db_path = config["paths"]["db_path"]

    def createConfig(self):
        config = configparser.ConfigParser()
        config["paths"] = {
            "db_path": os.path.join(
                os.path.expanduser("~"),
                ".local",
                "share",
                "assignment-list-pyqt5",
                "data.db"
            )
        }

        # Attempt to create directory if necessary
        if not os.path.exists(os.path.dirname(self.config_path)):
            try:
                os.mkdir(os.path.dirname(self.config_path))
            except:
                print("Error: Could not create config directory '{}'".format(os.path.dirname(self.config_path)))
                sys.exit(1)

        # Attempt to create file
        try:
            with open(self.config_path, 'w') as configfile:
                config.write(configfile)
        except:
            print("Error: Could not open config file '{}'".format(self.config_path))
            sys.exit(1)

        print("Successfully created config at {}".format(self.config_path))

if __name__ == "__main__":
    Config()
