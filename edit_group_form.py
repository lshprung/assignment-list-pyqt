import sys
from PyQt5.QtWidgets import QApplication, QComboBox, QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from add_entry_form import Globals
from group import Group
DB = __import__("db_sqlite")

class editGroupForm(QDialog):
    """
    Implemented so that it can be used for adding and editing groups
    """
    def __init__(self, id):
        self.id = id
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.resize(400, 1)
        self.setWindowTitle("Edit Group")
        self.displayWidgets()
        self.exec()

    def displayWidgets(self):
        group_form_layout = QFormLayout()
        group = list(filter(lambda g: g.id == self.id, Globals.groups))[0]

        title = QLabel("Edit Group")
        title.setFont(QFont("Arial", 18))
        title.setAlignment(Qt.AlignCenter)
        group_form_layout.addRow(title)

        self.group_name = QLineEdit()
        self.group_name.setText(group.name)
        group_form_layout.addRow("Name:", self.group_name)

        self.group_column = QComboBox()
        self.group_column.addItems(["Left", "Right"])
        self.group_column.setCurrentIndex(0 if group.column.lower() == "left" else 1)
        group_form_layout.addRow("Column:", self.group_column)

        self.group_link = QLineEdit() # TODO see if there is a widget specifically for URLs
        self.group_link.setText(group.link)
        group_form_layout.addRow("Link:", self.group_link)

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
        name_text = self.group_name.text()
        column_text = self.group_column.currentText()
        link_text = self.group_link.text()

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
        Globals.groups.append(Group(self.id, name_text, column_text, link_text))
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = editGroupForm()
    sys.exit(app.exec_())
