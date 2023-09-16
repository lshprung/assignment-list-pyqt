#!/usr/bin/python3
import sys
import time
from PyQt5.QtWidgets import QAction, QApplication, QHBoxLayout, QLabel, QMainWindow, QMessageBox, QPushButton, QToolBar, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from add_group_form import addGroupForm
from edit_group_form import editGroupForm
from add_entry_form import addEntryForm
from edit_entry_form import editEntryForm
Globals = __import__("globals")
DB = __import__("db_sqlite")

class AssignmentList(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.resize(640, 480)
        self.setWindowTitle("Assignment List")
        self.createMenu()
        self.createToolbar()
        self.setupDB()
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
        edit_menu.addSeparator()
        self.clean_hidden_act = QAction("Permanently Delete Removed Groups and Entries", self)
        self.clean_hidden_act.triggered.connect(self.cleanHidden)
        edit_menu.addAction(self.clean_hidden_act)

        about_act = QAction("About", self)
        about_act.triggered.connect(self.aboutDialog)
        help_menu.addAction(about_act)

    def createToolbar(self):
        tool_bar = QToolBar("Toolbar")
        self.addToolBar(tool_bar)

        tool_bar.addAction(self.add_group_act)

    def setupDB(self):
        DB.initDB()

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

    def editGroup(self, id):
        """
        Open the 'editGroup' form
        """
        self.create_edit_group_dialog = editGroupForm(id)
        self.drawGroups()

    def removeGroup(self, id):
        """
        Delete a group with a given id
        """
        # TODO might want to add a warning
        # TODO might want to make part of the a destructor in the Group class
        removed = DB.removeGroup(id)
        if removed > 0:
            Globals.entries = list(filter(lambda e: e.parent_id != id, Globals.entries))
            Globals.groups = list(filter(lambda g: g.id != id, Globals.groups))
            self.drawGroups()

    def addEntry(self, parent):
        """
        Open the 'addEntry' form
        """
        old_count = len(Globals.entries)
        self.create_new_entry_dialog = addEntryForm(parent)
        if old_count != len(Globals.entries):
            self.drawGroups() # TODO see if we can do this with only redrawing a single group

    def editEntry(self, id):
        """
        Open the 'editEntry' form
        """
        self.create_edit_entry_dialog = editEntryForm(id)
        self.drawGroups()

    def toggleDoneEntry(self, id):
        """
        Toggle the 'done' flag on the entry with the given id
        """
        entry = list(filter(lambda e: e.id == id, Globals.entries))[0]
        if entry.done:
            entry.done = False
        else:
            entry.done = True
        DB.updateEntry(entry)
        Globals.entries = list(filter(lambda e: e.id != id, Globals.entries))
        Globals.entries.append(entry)
        self.drawGroups()

    def removeEntry(self, id):
        """
        Delete an entry with a given id
        """
        # TODO might want to add a warning
        # TODO might want to make part of the a destructor in the Entry class
        removed = DB.removeEntry(id)
        if removed > 0:
            Globals.entries = list(filter(lambda e: e.id != id, Globals.entries))
            self.drawGroups()

    def cleanHidden(self):
        """
        Permanently delete removed groups and entries from db
        """
        # TODO consider creating a warning dialogue for this
        DB.cleanHidden()

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

        # Sort the groups
        Globals.groups = sorted(Globals.groups, key=lambda g: g.id)

        # Sort the entries (by due_date for now)
        Globals.entries = sorted(Globals.entries, key=lambda e: (e.parent_id, e.due, e.id))

        # Create columns as vertical boxes
        column_left = QVBoxLayout()
        column_right = QVBoxLayout()

        for g in Globals.groups:
            # skip if this group is set to hidden
            if g.hidden:
                continue

            g_layout = g.buildLayout()
            
            # Draw entries belonging to this group
            g_layout.addLayout(self.drawEntries(g.id))

            # Include buttons at the bottom to edit the group
            buttons_hbox = QHBoxLayout()

            add_entry_button = QPushButton()
            add_entry_button.setText("Add Entry")
            add_entry_button.clicked.connect((lambda id: lambda: self.addEntry(id))(g.id))
            buttons_hbox.addWidget(add_entry_button)

            edit_group_button = QPushButton()
            edit_group_button.setText("Edit Group")
            edit_group_button.clicked.connect((lambda id: lambda: self.editGroup(id))(g.id))
            buttons_hbox.addWidget(edit_group_button)

            del_group_button = QPushButton()
            del_group_button.setText("Remove Group")
            del_group_button.clicked.connect((lambda id: lambda: self.removeGroup(id))(g.id))
            buttons_hbox.addWidget(del_group_button)

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

    def drawEntries(self, group_id):
        """
        Redraw the entries of a specific group
        """
        # TODO consider having code to remove existing widgets to make this function more modular
        entries = list(filter(lambda e: e.parent_id == group_id, Globals.entries))
        entries_vbox = QVBoxLayout()
        entries_vbox.setContentsMargins(5, 0, 0, 0)

        for e in entries:
            # skip if this entry is set to hidden
            if e.hidden:
                continue

            entries_vbox.addLayout(e.buildLayout())

            # entry modifier buttons
            buttons_hbox = QHBoxLayout()

            edit_entry_button = QPushButton()
            edit_entry_button.setText("Edit Entry")
            edit_entry_button.clicked.connect((lambda id: lambda: self.editEntry(id))(e.id))
            buttons_hbox.addWidget(edit_entry_button)

            mark_done_button = QPushButton()
            if e.done:
                mark_done_button.setText("Not Done")
            else:
                mark_done_button.setText("Done")
            mark_done_button.clicked.connect((lambda id: lambda: self.toggleDoneEntry(id))(e.id))
            buttons_hbox.addWidget(mark_done_button)

            del_entry_button = QPushButton()
            del_entry_button.setText("Remove Entry")
            del_entry_button.clicked.connect((lambda id: lambda: self.removeEntry(id))(e.id))
            buttons_hbox.addWidget(del_entry_button)

            buttons_hbox.addStretch()
            entries_vbox.addLayout(buttons_hbox)

        return entries_vbox

    def aboutDialog(self):
        QMessageBox.about(self, "About Assignment List",
                          "Created by Louie S. - 2023")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AssignmentList()
    sys.exit(app.exec_())

