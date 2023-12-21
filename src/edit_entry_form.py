import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import QDate

import src.globals as Globals
from src.entry import Entry
import src.db_sqlite as DB

# Reuses the add_entry_form UI file
class editEntryForm(QDialog):
    """
    Form to edit/update an entry
    """
    def __init__(self, id):
        self.id = id
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                   "add_entry_form.ui"), self)
        self.initializeUI()

    def initializeUI(self):
        self.setWindowTitle("Edit Entry")
        self.displayWidgets()
        self.exec()

    def displayWidgets(self):
        entry = list(filter(lambda e: e.id == self.id, Globals.entries))[0]

        self.title.setText("Edit Entry")
        self.new_entry_desc.setText(entry.desc)
        self.new_entry_due.setDate(QDate.currentDate())
        if entry.due:
            self.new_entry_due.setDate(entry.due)
            self.new_entry_due_checkbox.setChecked(True)
        else:
            self.new_entry_due_checkbox.setChecked(False)
        self.new_entry_due_alt.setText(entry.due_alt)
        self.new_entry_link.setText(entry.link)
        self.new_entry_color.setText(entry.color)
        self.new_entry_highlight.setText(entry.highlight)
        self.buttonBox.rejected.connect(self.close)
        self.buttonBox.accepted.connect(self.handleSubmit)

    def handleSubmit(self):
        desc_text = self.new_entry_desc.text()
        if self.new_entry_due_checkbox.isChecked():
            due_text = self.new_entry_due.date() # due_text is a QDate
        else:
            due_text = "" # due is unchecked
        due_alt_text = self.new_entry_due_alt.text()
        link_text = self.new_entry_link.text()
        color_text = self.new_entry_color.text()
        highlight_text = self.new_entry_highlight.text()

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
        entry.color = color_text
        entry.highlight = highlight_text
        DB.updateEntry(entry)

        # Update global variables
        Globals.entries = list(filter(lambda e: e.id != self.id, Globals.entries))
        Globals.entries.append(Entry(self.id, entry.parent_id, desc_text, due_text, due_alt_text, link_text, color_text, highlight_text, entry.done, entry.hidden))
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = editEntryForm()
    sys.exit(app.exec_())

