from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QVBoxLayout
Globals = __import__("globals")

class Group:
    def __init__(self, id, name, column = "left", link = "", hidden = False):
        self.id = id
        self.name = name
        self.column = column
        self.link = link
        self.hidden = hidden

    def buildLayout(self):
        output = QVBoxLayout()
        output.setContentsMargins(0, 10, 0, 10)

        name = QLabel(self.name)
        name.setTextInteractionFlags(Qt.TextSelectableByMouse)
        name_font = QFont("Arial", 13)
        name_font.setUnderline(True)
        name.setFont(name_font)
        output.addWidget(name)

        return output
