import sys
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QApplication, QDialog, QHBoxLayout, QPushButton, QScrollArea, QVBoxLayout
from assignment_list_pyqt.config import Config
from assignment_list_pyqt.rule import Rule
import assignment_list_pyqt.db_sqlite as DB
import assignment_list_pyqt.globals as Globals

class RulesDialog(QDialog):
    """
    Show the list of rules associated with an entry
    """
    def __init__(self, entry_id):
        super().__init__()
        
        self.entry_id = entry_id
        # class globals
        self.config = Config()
        self.relevant_rules = self.getRelevantRules()

        self.initializeUI()

    def initializeUI(self):
        self.resize(500, 320)
        self.setWindowTitle("Rules")
        self.displayWidgets()
        self.exec()

    def displayWidgets(self):
        main_layout = QVBoxLayout()
        main_layout_scroll_area = QScrollArea()
        main_layout_scroll_area.setWidgetResizable(True)
        main_layout_scroll_area.setLayout(main_layout)

        self.rules_layout = QVBoxLayout()
        self.drawRules()
        main_layout.addLayout(self.rules_layout)
        
        main_layout.addStretch()
        # Create Close and Save buttons
        buttons_hbox = QHBoxLayout()
        buttons_hbox.addStretch()

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        buttons_hbox.addWidget(close_button)

        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save)
        buttons_hbox.addWidget(save_button)

        main_layout.addLayout(buttons_hbox)
        self.setLayout(main_layout)

    def drawRules(self):
        # Remove all children from layout
        def recursiveClear(layout):
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
                elif child.layout():
                    recursiveClear(child)

        recursiveClear(self.rules_layout)

        # Draw each rule
        self.r_layouts_dict = {} # Use to help update things in the save() function
        for r in self.relevant_rules:
            r_layout = r.buildLayout()
            self.r_layouts_dict[r.id] = r_layout
            del_button = QPushButton("Delete", self)
            del_button.clicked.connect((lambda id: lambda: self.deleteRule(id))(r.id))
            r_layout.addWidget(del_button)
            self.rules_layout.addLayout(r_layout)

        # Draw a button to add rules
        rules_buttons_hbox = QHBoxLayout()
        add_rule_button = QPushButton("Add Rule", self)
        add_rule_button.clicked.connect(self.addRule)
        rules_buttons_hbox.addWidget(add_rule_button)
        rules_buttons_hbox.addStretch()
        self.rules_layout.addLayout(rules_buttons_hbox)

    def addRule(self):
        self.apply()

        new_rule = Rule(0, self.entry_id, "before", QDate.currentDate())
        new_rule_id = DB.insertRule(new_rule)
        new_rule.id = new_rule_id
        Globals.rules.append(new_rule)
        self.relevant_rules = self.getRelevantRules()
        self.drawRules()

    def deleteRule(self, rule_id):
        DB.removeRule(rule_id)
        Globals.rules = list(filter(lambda r: r.id != rule_id, Globals.rules))
        self.relevant_rules = self.getRelevantRules()
        self.drawRules()

    def getRelevantRules(self):
        return list(filter(lambda r: r.entry_id == self.entry_id, Globals.rules))

    def apply(self):
        for id, layout in self.r_layouts_dict.items():
            updated_rule = Rule(
                id,
                self.entry_id,
                layout.itemAt(0).widget().currentText(),
                layout.itemAt(1).widget().date(),
                layout.itemAt(3).widget().text(),
                layout.itemAt(4).widget().text())
            DB.updateRule(updated_rule)
            Globals.rules = list(filter(lambda r: r.id != id, Globals.rules))
            Globals.rules.append(updated_rule)

    def save(self):
        """
        Save any existing rules. Added rules are automatically saved, 
        but changing rules is not, hence the need for a manual save
        """
        self.apply()
        self.done(1)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RulesDialog()
    sys.exit(app.exec_())
