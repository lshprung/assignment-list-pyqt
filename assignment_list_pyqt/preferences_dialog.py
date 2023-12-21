import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
from assignment_list_pyqt.config import Config

class PreferencesDialog(QDialog):
    """
    Implemented to set configuration options in the program
    """
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                   "preferences_dialog.ui"), self)
        
        # class globals
        self.config = Config()

        self.initializeUI()

    def initializeUI(self):
        self.displayWidgets()
        self.exec()

    def displayWidgets(self):
        # TODO make this a scrollable window
        # FIXME could use some work on sizing
        self.pathsTabLayout()

        self.close_button.clicked.connect(self.close)
        self.apply_button.clicked.connect(self.apply)
        self.reload_button.clicked.connect(self.reload)

    def pathsTabLayout(self):
        if "paths" in self.config.config:
            self.db_path_edit.setText(self.config.config["paths"]["db_path"])
        self.db_path_button.clicked.connect(self.dbPathDialog)

    def dbPathDialog(self):
        file_dialog = QFileDialog(self)
        # TODO create filter to only allow selecting .db files
        new_path = file_dialog.getOpenFileName(self, "Open File")

        if new_path[0]:
            self.db_path_edit.setText(new_path[0])

    def apply(self):
        """
        Update the configuration in the config file
        """
        # Save paths
        if "paths" in self.config.config:
            try:
                with open(self.db_path_edit.text(), 'a'):
                    self.config.config["paths"]["db_path"] = self.db_path_edit.text()
            except:
                print("Warning: db_path '{}' does not exist; skipping".format(self.db_path_edit.text()))

        self.config.updateConfig()

    def reload(self):
        """
        Update, reload, and close the window
        """
        self.apply()
        self.done(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PreferencesDialog()
    sys.exit(app.exec_())
