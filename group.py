import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout
from add_entry_form import addEntryForm
from entry import Entry

class Group:
    def __init__(self, name, column = "left", link = ""):
        self.name = name
        self.column = column
        self.link = link

    def buildLayout(self):
        output = QVBoxLayout()
        output.setContentsMargins(0, 10, 0, 10)

        name = QLabel(self.name)
        name.setTextInteractionFlags(Qt.TextSelectableByMouse)
        name_font = QFont("Arial", 13)
        name_font.setUnderline(True)
        name.setFont(name_font)
        output.addWidget(name)

        entries = self.getEntriesFromGroup()
        entries_vbox = QVBoxLayout()
        entries_vbox.setContentsMargins(5, 0, 0, 0)

        for e in entries:
            entries_vbox.addWidget(e.buildLayout())
        output.addLayout(entries_vbox)

        # Include buttons at the bottom to edit the group
        buttons_hbox = QHBoxLayout()

        add_entry_button = QPushButton()
        add_entry_button.setText("Add Entry")
        add_entry_button.clicked.connect(self.addEntry)
        buttons_hbox.addWidget(add_entry_button)
        buttons_hbox.addStretch()

        output.addLayout(buttons_hbox)

        return output

    def addEntry(self):
        """
        Open the 'addEntry' form
        """
        self.create_new_entry_dialog = addEntryForm()
        self.create_new_entry_dialog.show()

    def getEntriesFromGroup(self):
        """
        Retrieve this group's entries
        """
        # TODO this should be pulling from a database
        output = []
        output.append(Entry("yeet"))
        output.append(Entry("bruh", datetime.date(2023, 12, 25)))

        return output
