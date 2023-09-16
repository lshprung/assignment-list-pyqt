import sys
from PyQt5.QtWidgets import QApplication, QCheckBox, QDateTimeEdit, QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate, Qt

Globals = __import__("globals")
from entry import Entry
DB = __import__("db_sqlite")

class editEntryForm(QDialog):
    """
    Form to edit/update an entry
    """
    def __init__(self, id):
        self.id = id
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.resize(400, 1)
        self.setWindowTitle("Edit Entry")
        self.displayWidgets()
        self.exec()

    def displayWidgets(self):
        entry_form_layout = QFormLayout()
        entry = list(filter(lambda e: e.id == self.id, Globals.entries))[0]

        title = QLabel("Edit Entry")
        title.setFont(QFont("Arial", 18))
        title.setAlignment(Qt.AlignCenter)
        entry_form_layout.addRow(title)

        self.entry_desc = QLineEdit()
        self.entry_desc.setText(entry.desc)
        entry_form_layout.addRow("Description:", self.entry_desc)

        self.due_hbox = QHBoxLayout()
        self.entry_due = QDateTimeEdit(QDate.currentDate())
        self.entry_due.setDisplayFormat("MM/dd/yyyy")
        if entry.due:
            self.entry_due.setDate(entry.due)
        self.due_hbox.addWidget(self.entry_due)
        self.entry_due_checkbox = QCheckBox()
        if entry.due:
            self.entry_due_checkbox.setChecked(True)
        else:
            self.entry_due_checkbox.setChecked(False)
        self.due_hbox.addWidget(self.entry_due_checkbox)
        entry_form_layout.addRow("Due Date:", self.due_hbox)

        self.entry_due_alt = QLineEdit()
        self.entry_due_alt.setText(entry.due_alt)
        entry_form_layout.addRow("Due Date (Alt):", self.entry_due_alt)

        self.entry_link = QLineEdit() # TODO see if there is a widget specifically for URLs
        self.entry_link.setText(entry.link)
        entry_form_layout.addRow("Link:", self.entry_link)

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

        entry_form_layout.addRow(buttons_h_box)

        self.setLayout(entry_form_layout)

    def handleSubmit(self):
        desc_text = self.entry_desc.text()
        if self.entry_due_checkbox.isChecked():
            due_text = self.entry_due.date() # due_text is a QDate
        else:
            due_text = "" # due is unchecked
        due_alt_text = self.entry_due_alt.text()
        link_text = self.entry_link.text()

        if not desc_text:
            QMessageBox.warning(self, "Error Message",
                                "Name cannot be blank",
                                QMessageBox.Close,
                                QMessageBox.Close)
            return

        # Update DB
        entry = list(filter(lambda e: e.id == self.id, Globals.entries))[0]
        entry.desc = desc_text
        entry.due = due_text
        entry.due_alt = due_alt_text
        entry.link = link_text
        DB.updateEntry(entry)

        # Update global variables
        Globals.entries = list(filter(lambda e: e.id != self.id, Globals.entries))
        Globals.entries.append(Entry(self.id, entry.parent_id, desc_text, due_text, due_alt_text, link_text, entry.done, entry.hidden))
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = editEntryForm()
    sys.exit(app.exec_())

