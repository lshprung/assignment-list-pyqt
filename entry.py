from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel

class Entry:
    def __init__(self, id, parent_id, desc, due = "", due_alt = "", link = "", color = "", highlight = "", done = False, hidden = False):
        self.id = id
        self.parent_id = parent_id
        self.desc = desc
        self.due = due
        self.due_alt = due_alt
        self.link = link
        self.color = color
        self.highlight = highlight
        self.done = done
        self.hidden = hidden

    def buildLayout(self):
        output = QHBoxLayout()
        bullet = QLabel()
        body = QLabel()

        bullet.setFont(QFont("Arial", 11))

        body.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
        body.setFont(QFont("Arial", 11))
        body.setWordWrap(True)
        body.setToolTip("Right-Click for actions")

        if self.done:
            bullet.setText("\u2713 ")
            bullet.setStyleSheet("""
                QLabel{
                    color: green;
                }
            """)
        else:
            bullet.setText("- ")
        output.addWidget(bullet)

        if self.due:
            body.setText("{0}/{1}/{2}: ".format(self.due.month(), self.due.day(), self.due.year()))
        if self.link:
            body.setOpenExternalLinks(True)
            body.setText(body.text() + "<a href=\"{0}\" style=\"color: {1}; text-decoration: none;\">".format(self.link, self.color if self.color else "default"))
        body.setText(body.text() + self.desc)
        if self.link:
            body.setText(body.text() + "</a>")
            body.setToolTip("{}".format(self.link))
        output.addWidget(body)

        output.addStretch()

        if self.done:
            font = body.font()
            font.setStrikeOut(True)
            body.setFont(font)
            body.setStyleSheet("""
                QLabel{
                    color: green;
                }
            """)

        else:
            body.setStyleSheet("""
                QLabel{{
                    color: {0};
                    background-color: {1};
                }}""".format(
                    self.color if self.color else "default",
                    self.highlight if self.highlight else "none"
                ))

        return output
