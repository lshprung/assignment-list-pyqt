#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import QApplication, QDateTimeEdit, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate, Qt

class addEntryForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.resize(400, 1)
        self.setWindowTitle("Add Entry")
        self.displayWidgets()
        self.show()

    def displayWidgets(self):
        entry_form_layout = QFormLayout()

        title = QLabel("Add Entry")
        title.setFont(QFont("Arial", 18))
        title.setAlignment(Qt.AlignCenter)
        entry_form_layout.addRow(title)

        new_entry_desc = QLineEdit()
        entry_form_layout.addRow("Description:", new_entry_desc)

        new_entry_due = QDateTimeEdit(QDate.currentDate())
        new_entry_due.setDisplayFormat("MM/dd/yyyy")
        entry_form_layout.addRow("Due Date:", new_entry_due)

        new_entry_due_alt = QLineEdit()
        entry_form_layout.addRow("Due Date (Alt):", new_entry_due_alt)

        new_entry_link = QLineEdit() # TODO see if there is a widget specifically for URLs
        entry_form_layout.addRow("Link:", new_entry_link)

        # TODO:
            # color
            # highlight
            # depends

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

        entry_form_layout.addRow(buttons_h_box)

        self.setLayout(entry_form_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = addEntryForm()
    sys.exit(app.exec_())
