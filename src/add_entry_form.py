import os
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtCore import QDate
from src.entry import Entry
import src.globals as Globals
import src.db_sqlite as DB

class addEntryForm(QDialog):
    def __init__(self, parent):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                   "add_entry_form.ui"), self)
        self.initializeUI(parent)

    def initializeUI(self, parent):
        self.displayWidgets(parent)
        self.exec()

    def displayWidgets(self, parent):
        self.new_entry_due.setDate(QDate.currentDate())
        self.buttonBox.rejected.connect(self.close)
        self.buttonBox.accepted.connect(lambda: self.handleSubmit(parent))

    def handleSubmit(self, parent):
        # Check that the new entry is not blank
        desc_text = self.new_entry_desc.text()
        due_text = ""
        if self.new_entry_due_checkbox.isChecked():
            due_text = self.new_entry_due.date() # due_text is a QDate
        due_alt_text = self.new_entry_due_alt.text()
        link_text = self.new_entry_link.text()
        color_text = self.new_entry_color.text()
        highlight_text = self.new_entry_highlight.text()

        if not desc_text:
            QMessageBox.warning(self, "Error Message",
                                "Description cannot be blank",
                                QMessageBox.Close,
                                QMessageBox.Close)
            return

        new_id = DB.insertEntry(Entry(0, parent, desc_text, due_text, due_alt_text, link_text, color_text, highlight_text))
        Globals.entries.append(Entry(new_id, parent, desc_text, due_text, due_alt_text, link_text, color_text, highlight_text))
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = addEntryForm()
    sys.exit(app.exec_())
