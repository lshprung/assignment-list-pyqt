from PyQt5.QtWidgets import QLabel, QVBoxLayout

class Group:
    def __init__(self, name, column = "left", link = ""):
        self.name = name
        self.column = column
        self.link = link

    def buildLayout(self):
        output = QVBoxLayout()
        output.setContentsMargins(0, 10, 0, 10)

        name = QLabel(self.name)
        output.addWidget(name)
        return output
