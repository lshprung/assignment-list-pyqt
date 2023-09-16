#!/usr/bin/python3
import sys
import time
from PyQt5.QtWidgets import QAction, QApplication, QHBoxLayout, QLabel, QMainWindow, QMessageBox, QPushButton, QToolBar, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from add_group_form import addGroupForm
from add_entry_form import addEntryForm
from entry import Entry
from group import Group
Globals = __import__("globals")

class AssignmentList(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.resize(640, 480)
        self.setWindowTitle("Assignment List")
        self.createMenu()
        self.createToolbar()
        self.displayWidgets()
        self.show()

    def createMenu(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")
        edit_menu = menu_bar.addMenu("Edit")
        help_menu = menu_bar.addMenu("Help")

        exit_act = QAction("Exit", self)
        exit_act.setShortcut("Ctrl+Q")
        exit_act.triggered.connect(self.close)
        file_menu.addAction(exit_act)

        self.add_group_act = QAction("Add Group", self)
        self.add_group_act.triggered.connect(self.addGroup)
        edit_menu.addAction(self.add_group_act)

        about_act = QAction("About", self)
        about_act.triggered.connect(self.aboutDialog)
        help_menu.addAction(about_act)

    def createToolbar(self):
        tool_bar = QToolBar("Toolbar")
        self.addToolBar(tool_bar)

        tool_bar.addAction(self.add_group_act)

    def displayWidgets(self):
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        title = QLabel(time.strftime("%A, %b %d %Y"))
        title.setFont(QFont("Arial", 17))
        title.setTextInteractionFlags(Qt.TextSelectableByMouse)

        title_h_box = QHBoxLayout()
        title_h_box.addStretch()
        title_h_box.addWidget(title)
        title_h_box.addStretch()

        self.load_groups()
        self.load_entries() # TODO placeholder, this will eventually be moved to group.py
        self.groups_hbox = QHBoxLayout()
        self.groups_hbox.setContentsMargins(20, 5, 20, 5)
        self.drawGroups()

        v_box = QVBoxLayout()
        v_box.addLayout(title_h_box)
        v_box.addLayout(self.groups_hbox)
        v_box.addStretch()

        main_widget.setLayout(v_box)

    def addGroup(self):
        """
        Open the 'addGroup' form
        """
        old_count = len(Globals.groups)
        self.create_new_group_dialog = addGroupForm()
        if old_count != len(Globals.groups):
            self.drawGroups()

    def addEntry(self, parent):
        """
        Open the 'addEntry' form
        """
        old_count = len(Globals.entries)
        self.create_new_entry_dialog = addEntryForm(parent)
        if old_count != len(Globals.entries):
            self.drawGroups() # TODO see if we can do this with only redrawing a single group


    def drawGroups(self):
        """
        Redraw the groups_hbox
        """
        # Remove all children from layout
        def recursiveClear(layout):
            while layout.count():
                child = layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()
                elif child.layout():
                    recursiveClear(child)

        recursiveClear(self.groups_hbox)

        # Create columns as vertical boxes
        column_left = QVBoxLayout()
        column_right = QVBoxLayout()

        for g in Globals.groups:
            # Include buttons at the bottom to edit the group
            g_layout = g.buildLayout()
            buttons_hbox = QHBoxLayout()
            add_entry_button = QPushButton()
            add_entry_button.setText("Add Entry")
            add_entry_button.clicked.connect((lambda id: lambda: self.addEntry(id))(g.id))
            buttons_hbox.addWidget(add_entry_button)
            buttons_hbox.addStretch()
            g_layout.addLayout(buttons_hbox)
            if g.column.lower() == "left":
                column_left.addLayout(g_layout)
            else:
                column_right.addLayout(g_layout)

        column_left.addStretch()
        column_right.addStretch()

        self.groups_hbox.addLayout(column_left)
        self.groups_hbox.addStretch()
        self.groups_hbox.addLayout(column_right)
        self.groups_hbox.addStretch()

    # Implementation should be moved here from group.py if possible
    def drawEntries(self):
        """
        Redraw the entries of a specific group
        """
        pass

    def aboutDialog(self):
        QMessageBox.about(self, "About Assignment List",
                          "Created by Louie S. - 2023")

    def load_groups(self):
        """
        Load groups data
        """
        Globals.groups.append(Group(1, "test1", "left"))
        Globals.groups.append(Group(2, "test2", "left"))
        Globals.groups.append(Group(3, "test3", "right"))
        Globals.groups.append(Group(4, "test4", "right"))

    def load_entries(self):
        """
        Load entries data
        """
        Globals.entries.append(Entry(1, "test1-task1"))
        Globals.entries.append(Entry(2, "test2-task1"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AssignmentList()
    sys.exit(app.exec_())

