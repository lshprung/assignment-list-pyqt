import sys
from PyQt5.QtWidgets import QApplication, QDateTimeEdit, QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate, Qt
from entry import Entry
Globals = __import__("globals")
DB = __import__("db_sqlite")

class addEntryForm(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.initializeUI(parent)

    def initializeUI(self, parent):
        self.resize(400, 1)
        self.setWindowTitle("Add Entry")
        self.displayWidgets(parent)
        self.exec()

    def displayWidgets(self, parent):
        entry_form_layout = QFormLayout()

        title = QLabel("Add Entry")
        title.setFont(QFont("Arial", 18))
        title.setAlignment(Qt.AlignCenter)
        entry_form_layout.addRow(title)

        self.new_entry_desc = QLineEdit()
        entry_form_layout.addRow("Description:", self.new_entry_desc)

        self.new_entry_due = QDateTimeEdit(QDate.currentDate())
        self.new_entry_due.setDisplayFormat("MM/dd/yyyy")
        entry_form_layout.addRow("Due Date:", self.new_entry_due)

        self.new_entry_due_alt = QLineEdit()
        entry_form_layout.addRow("Due Date (Alt):", self.new_entry_due_alt)

        self.new_entry_link = QLineEdit() # TODO see if there is a widget specifically for URLs
        entry_form_layout.addRow("Link:", self.new_entry_link)

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
        submit_button.clicked.connect(lambda: self.handleSubmit(parent)) # TODO connect this to a real method
        buttons_h_box.addWidget(submit_button)
        buttons_h_box.addStretch()

        entry_form_layout.addRow(buttons_h_box)

        self.setLayout(entry_form_layout)

    def handleSubmit(self, parent):
        # Check that the new entry is not blank
        desc_text = self.new_entry_desc.text()
        due_text = self.new_entry_due.date() # due_text is a QDate
        due_alt_text = self.new_entry_due_alt.text()
        link_text = self.new_entry_link.text()

        if not desc_text:
            QMessageBox.warning(self, "Error Message",
                                "Description cannot be blank",
                                QMessageBox.Close,
                                QMessageBox.Close)
            return

        new_id = DB.insertEntry(Entry(0, parent, desc_text, due_text, due_alt_text, link_text))
        Globals.entries.append(Entry(new_id, parent, desc_text, due_text, due_alt_text, link_text))
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = addEntryForm()
    sys.exit(app.exec_())
