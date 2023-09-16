import time
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel

class Entry:
    def __init__(self, parent_id, desc, due = "", due_alt = "", link = ""):
        self.parent_id = parent_id
        self.desc = desc
        self.due = due
        self.due_alt = due_alt
        self.link = link
        self.done = False

    def buildLayout(self):
        output = QLabel()
        output.setTextInteractionFlags(Qt.TextSelectableByMouse)
        output.setFont(QFont("Arial", 11))

        output.setText("- ")
        if(self.due):
            output.setText(output.text() + time.strftime("%m/%d/%y: "))
        output.setText(output.text() + self.desc)

        return output
