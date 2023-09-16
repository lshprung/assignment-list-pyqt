import time
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel

class Entry:
    def __init__(self, id, parent_id, desc, due = "", due_alt = "", link = "", done = False, hidden = False):
        self.id = id
        self.parent_id = parent_id
        self.desc = desc
        self.due = due
        self.due_alt = due_alt
        self.link = link
        self.done = done
        self.hidden = hidden

    def buildLayout(self):
        output = QLabel()
        output.setTextInteractionFlags(Qt.TextSelectableByMouse)
        output.setFont(QFont("Arial", 11))

        output.setText("- ")
        if(self.due):
            output.setText(output.text() + "{0}/{1}/{2}: ".format(self.due.month(), self.due.day(), self.due.year()))
        output.setText(output.text() + self.desc)

        return output
