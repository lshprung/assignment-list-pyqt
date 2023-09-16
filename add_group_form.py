#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import QApplication, QComboBox, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class addGroupForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.resize(400, 1)
        self.setWindowTitle("Add Group")
        self.displayWidgets()
        self.show()

    def displayWidgets(self):
        group_form_layout = QFormLayout()

        title = QLabel("Add Group")
        title.setFont(QFont("Arial", 18))
        title.setAlignment(Qt.AlignCenter)
        group_form_layout.addRow(title)

        new_group_name = QLineEdit()
        group_form_layout.addRow("Name:", new_group_name)

        new_group_column = QComboBox()
        new_group_column.addItems(["Left", "Right"])
        group_form_layout.addRow("Column:", new_group_column)

        new_group_link = QLineEdit() # TODO see if there is a widget specifically for URLs
        group_form_layout.addRow("Link:", new_group_link)

        # Submit and cancel buttons
        buttons_h_box = QHBoxLayout()
        buttons_h_box.addStretch()
        close_button = QPushButton("Cancel")
        close_button.clicked.connect(self.close)
        buttons_h_box.addWidget(close_button)
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.close) # TODO connect this to a real method
        buttons_h_box.addWidget(submit_button)
        buttons_h_box.addStretch()

        group_form_layout.addRow(buttons_h_box)

        self.setLayout(group_form_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = addGroupForm()
    sys.exit(app.exec_())
