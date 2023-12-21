import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

import src.globals as Globals
from src.group import Group
import src.db_sqlite as DB

class addGroupForm(QDialog):
    """
    Implemented so that it can be used for adding and editing groups
    """
    def __init__(self):
        super().__init__()
        uic.loadUi(os.path.join("src", "add_group_form.ui"), self)
        self.initializeUI()

    def initializeUI(self):
        self.displayWidgets()
        self.exec()

    def displayWidgets(self):
        self.buttonBox.rejected.connect(self.close)
        self.buttonBox.accepted.connect(self.handleSubmit)

    def handleSubmit(self):
        name_text = self.new_group_name.text()
        column_text = self.new_group_column.currentText()
        link_text = self.new_group_link.text()

        if not name_text:
            QMessageBox.warning(self, "Error Message",
                                "Name cannot be blank",
                                QMessageBox.Close,
                                QMessageBox.Close)
            return

        new_id = DB.insertGroup(Group(0, name_text, column_text, link_text))
        Globals.groups.append(Group(new_id, name_text, column_text, link_text))
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = addGroupForm()
    sys.exit(app.exec_())
