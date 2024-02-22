from datetime import date
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLabel
import assignment_list_pyqt.globals as Globals

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

        output.setContentsMargins(2,2,2,2)

        bullet.setFont(QFont("Arial", 11))
        bullet.setMaximumWidth(15)

        body.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)
        body.setFont(QFont("Arial", 11))
        body.setWordWrap(True)
        body.setToolTip("Right-Click for actions")

        # Check rules
        relevant_rules = list(filter(lambda r: r.entry_id == self.id, Globals.rules))
        for r in relevant_rules:
            if (r.when.lower() == "before" and r.date > QDate.currentDate()) or (r.when.lower() == "after" and r.date <= QDate.currentDate()):
                if r.color:
                    self.color = r.color
                if r.highlight:
                    self.highlight = r.highlight

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
            body.setText("{0}/{1}/{2}: ".format(
                self.due.month(), 
                self.due.day(), 
                self.due.year()
            ))
        elif self.due_alt:
            body.setText("{0}: ".format(
                self.due_alt
            ))
        if self.link:
            body.setOpenExternalLinks(True)
            body.setText(body.text() + "<a href=\"{0}\" style=\"color: {1};\">".format(
                self.link, 
                self.color if self.color else "default"
            ))
        body.setText(body.text() + self.desc)
        if self.link:
            body.setText(body.text() + "</a>")
            body.setToolTip("{}".format(self.link))
        output.addWidget(body)

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
                    font-weight: {2};
                }}""".format(
                    self.color if self.color else "default",
                    self.highlight if self.highlight else "none",
                    "bold" if self.due and self.due <= date.today() else "normal"
                ))

        return output
