"""
Handle reading of the config file, which on POSIX-compliant systems will be
created in ~/.config/assignment-list-pyqt5/config.py
"""

import configparser
import os
import sys

import src.globals as Globals

class Config():
    def __init__(self):
        self.config_path = self.getConfigPath()

        if not os.path.exists(self.config_path):
            self.createConfig()

        self.loadConfig()

    def getConfigPath(self):
        # Windows config path is "$LOCALAPPDATA/assignment-list-pyqt5/config"
        if sys.platform.startswith("win32"):
            return os.path.join(os.path.expandvars("$LOCALAPPDATA"), 
                                "assignment-list-pyqt5",
                                "config")
        # Unix config path is "$HOME/.config/assignment-list-pyqt5/config"
        else:
            return os.path.join(
                os.path.expanduser("~"),
                ".config",
                "assignment-list-pyqt5",
                "config")

    def loadConfig(self):
        self.config = configparser.ConfigParser()

        try:
            self.config.read(self.config_path)
        except:
            print("Could not parse config file '{}'".format(self.config_path))
        
        if "paths" in self.config:
            if self.config["paths"]["db_path"]:
                Globals.db_path = self.config["paths"]["db_path"]

    def createConfig(self):
        self.config = configparser.ConfigParser()
        if sys.platform.startswith("win32"):
            self.config["paths"] = {
                # Windows default DB path is "$APPDATA/assignment-list-pyqt5/data.db"
                "db_path": os.path.join(
                    os.path.expandvars("$APPDATA"),
                    "assignment-list-pyqt5",
                    "data.db"
                )
            }
        else:
            self.config["paths"] = {
                # Unix default DB path is "$HOME/.local/share/assignment-list-pyqt5/data.db"
                "db_path": os.path.join(
                    os.path.expanduser("~"),
                    ".local",
                    "share",
                    "assignment-list-pyqt5",
                    "data.db"
                )
            }

        self.updateConfig()

    def updateConfig(self):
        """
        Update the configuration file with values from self.config
        """
        # Attempt to create directory if necessary
        if not os.path.exists(os.path.dirname(self.config_path)):
            try:
                os.mkdir(os.path.dirname(self.config_path))
            except:
                print("Error: Could not create config directory '{}'".format(os.path.dirname(self.config_path)))
                sys.exit(1)

        # Attempt to write to file
        try:
            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)
        except:
            print("Error: Could not open config file '{}'".format(self.config_path))
            sys.exit(1)

        print("Successfully created config at {}".format(self.config_path))

if __name__ == "__main__":
    Config()
