import sys
from PyQt5.QtWidgets import QApplication, QCheckBox, QDateTimeEdit, QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QDate, Qt
from src.entry import Entry
import src.globals as Globals
import src.db_sqlite as DB

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

        self.due_hbox = QHBoxLayout()
        self.new_entry_due = QDateTimeEdit(QDate.currentDate())
        self.new_entry_due.setDisplayFormat("MM/dd/yyyy")
        self.due_hbox.addWidget(self.new_entry_due)
        self.new_entry_due_checkbox = QCheckBox()
        self.new_entry_due_checkbox.setChecked(True)
        self.due_hbox.addWidget(self.new_entry_due_checkbox)
        entry_form_layout.addRow("Due Date:", self.due_hbox)

        self.new_entry_due_alt = QLineEdit()
        entry_form_layout.addRow("Due Date (Alt):", self.new_entry_due_alt)

        self.new_entry_link = QLineEdit() # TODO see if there is a widget specifically for URLs
        entry_form_layout.addRow("Link:", self.new_entry_link)

        # TODO:
            # depends

        self.new_entry_color = QLineEdit()
        entry_form_layout.addRow("Color:", self.new_entry_color)

        self.new_entry_highlight = QLineEdit()
        entry_form_layout.addRow("Highlight:", self.new_entry_highlight)

        # Submit and cancel buttons
        buttons_h_box = QHBoxLayout()
        buttons_h_box.addStretch()
        close_button = QPushButton("Cancel")
        close_button.clicked.connect(self.close)
        buttons_h_box.addWidget(close_button)
        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(lambda: self.handleSubmit(parent))
        buttons_h_box.addWidget(submit_button)
        buttons_h_box.addStretch()

        entry_form_layout.addRow(buttons_h_box)

        self.setLayout(entry_form_layout)

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
