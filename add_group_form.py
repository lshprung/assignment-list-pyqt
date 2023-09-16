import sys
from PyQt5.QtWidgets import QApplication, QComboBox, QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from add_entry_form import Globals
from group import Group
DB = __import__("db_sqlite")

class addGroupForm(QDialog):
    """
    Implemented so that it can be used for adding and editing groups
    """
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.resize(400, 1)
        self.setWindowTitle("Add Group")
        self.displayWidgets()
        self.exec()

    def displayWidgets(self):
        group_form_layout = QFormLayout()

        title = QLabel("Add Group")
        title.setFont(QFont("Arial", 18))
        title.setAlignment(Qt.AlignCenter)
        group_form_layout.addRow(title)

        self.new_group_name = QLineEdit()
        group_form_layout.addRow("Name:", self.new_group_name)

        self.new_group_column = QComboBox()
        self.new_group_column.addItems(["Left", "Right"])
        group_form_layout.addRow("Column:", self.new_group_column)

        self.new_group_link = QLineEdit() # TODO see if there is a widget specifically for URLs
        group_form_layout.addRow("Link:", self.new_group_link)

        # Submit and cancel buttons
        buttons_h_box = QHBoxLayout()
        buttons_h_box.addStretch()
        close_button = QPushButton("Cancel")
        close_button.clicked.connect(self.close)
        buttons_h_box.addWidget(close_button)
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.handleSubmit)
        buttons_h_box.addWidget(submit_button)
        buttons_h_box.addStretch()

        group_form_layout.addRow(buttons_h_box)

        self.setLayout(group_form_layout)

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
        # TODO do the database stuff (this will allow us to get the id)
        Globals.groups.append(Group(new_id, name_text, column_text, link_text))
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = addGroupForm()
    sys.exit(app.exec_())
