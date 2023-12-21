
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QComboBox, QDateTimeEdit, QHBoxLayout, QLineEdit


class Rule:
    def __init__(self, id, entry_id, when, date, color = "", highlight = ""):
        self.id = id
        self.entry_id = entry_id
        self.when = when
        self.date = date
        self.color = color
        self.highlight = highlight

    def buildLayout(self):
        output = QHBoxLayout()
        
        when_widget = QComboBox()
        when_widget.addItems(["Before", "After"])
        when_widget.setCurrentIndex(0 if self.when.lower() == "before" else 1)
        output.addWidget(when_widget)

        date_widget = QDateTimeEdit(QDate.currentDate())
        date_widget.setDisplayFormat("MM/dd/yyyy")
        date_widget.setDate(self.date)
        output.addWidget(date_widget)

        output.addStretch()

        # TODO Consider making this a color selector widget
        color_widget = QLineEdit()
        color_widget.setPlaceholderText("Color")
        if self.color:
            color_widget.setText(self.color)
        output.addWidget(color_widget)

        # TODO Consider making this a color selector widget
        highlight_widget = QLineEdit()
        highlight_widget.setPlaceholderText("Highlight")
        if self.highlight:
            highlight_widget.setText(self.highlight)
        output.addWidget(highlight_widget)

        return output
