from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel

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
        output = QHBoxLayout()
        bullet = QLabel()
        body = QLabel()

        body.setTextInteractionFlags(Qt.TextSelectableByMouse)

        bullet.setFont(QFont("Arial", 11))
        body.setFont(QFont("Arial", 11))

        if self.done:
            bullet.setText("\u2713 ")
        else:
            bullet.setText("- ")
        output.addWidget(bullet)

        if(self.due):
            body.setText("{0}/{1}/{2}: ".format(self.due.month(), self.due.day(), self.due.year()))
        body.setText(body.text() + self.desc)
        output.addWidget(body)

        output.addStretch()

        if self.done:
            font = body.font()
            font.setStrikeOut(True)
            body.setFont(font)

        return output
