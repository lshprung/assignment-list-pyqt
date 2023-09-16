import sys
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog, QFormLayout, QHBoxLayout, QLineEdit, QPushButton, QTabWidget, QVBoxLayout, QWidget
from src.config import Config

class PreferencesDialog(QDialog):
    """
    Implemented to set configuration options in the program
    """
    def __init__(self):
        super().__init__()
        
        # class globals
        self.config = Config()

        self.initializeUI()

    def initializeUI(self):
        self.resize(500, 320)
        self.setWindowTitle("Preferences")
        self.displayWidgets()
        self.exec()

    def displayWidgets(self):
        # TODO make this a scrollable window
        # FIXME could use some work on sizing
        main_layout = QVBoxLayout()
        tab_bar = QTabWidget(self)
        paths_tab = self.pathsTabLayout()

        tab_bar.addTab(paths_tab, "Paths")
        main_layout.addWidget(tab_bar)
        main_layout.addStretch()

        buttons_hbox = QHBoxLayout()
        buttons_hbox.addStretch()

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        buttons_hbox.addWidget(close_button)

        apply_button = QPushButton("Apply", self)
        apply_button.clicked.connect(self.apply)
        buttons_hbox.addWidget(apply_button)
        
        main_layout.addLayout(buttons_hbox)
        self.setLayout(main_layout)

    def pathsTabLayout(self):
        output = QWidget()
        output_layout = QFormLayout()

        # Dialog for setting the database file path
        db_path_hbox = QHBoxLayout()
        self.db_path_edit = QLineEdit()
        if "paths" in self.config.config:
            self.db_path_edit.setText(self.config.config["paths"]["db_path"])
        db_path_hbox.addWidget(self.db_path_edit)
        db_path_button = QPushButton("...")
        db_path_button.setMaximumWidth(25)
        db_path_button.clicked.connect(self.dbPathDialog)
        db_path_hbox.addWidget(db_path_button)
        output_layout.addRow("Database File:", db_path_hbox)

        output.setLayout(output_layout)
        return output

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PreferencesDialog()
    sys.exit(app.exec_())
