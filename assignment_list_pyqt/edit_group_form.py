import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

import assignment_list_pyqt.globals as Globals
from assignment_list_pyqt.group import Group
import assignment_list_pyqt.db_sqlite as DB

class editGroupForm(QDialog):
    """
    Form to edit/update a group
    """
    def __init__(self, id):
        self.id = id
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                   "add_group_form.ui"), self)
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Edit Group")
        self.displayWidgets()
        self.exec()

    def displayWidgets(self):
        group = list(filter(lambda g: g.id == self.id, Globals.groups))[0]

        self.title.setText("Edit Group")
        self.new_group_name.setText(group.name)
        self.new_group_column.setCurrentIndex(0 if group.column.lower() == "left" else 1)
        self.new_group_link.setText(group.link)
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

        # Update DB
        group = list(filter(lambda g: g.id == self.id, Globals.groups))[0]
        group.name = name_text
        group.column = column_text
        group.link = link_text
        DB.updateGroup(group)

        # Update global variables
        Globals.groups = list(filter(lambda g: g.id != self.id, Globals.groups))
        Globals.groups.append(Group(self.id, name_text, column_text, link_text, group.hidden))
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = editGroupForm()
    sys.exit(app.exec_())
