#!/usr/bin/python3
import sys
import time
from PyQt5.QtWidgets import QAction, QApplication, QHBoxLayout, QLabel, QMainWindow, QMessageBox, QToolBar, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from add_group_form import addGroupForm
from group import Group

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
        self.create_new_group_dialog = addGroupForm()
        self.create_new_group_dialog.show()

    def drawGroups(self):
        """
        Redraw the groups_hbox
        """
        # Reset layout
        self.groups_hbox = QHBoxLayout()
        self.groups_hbox.setContentsMargins(20, 5, 20, 5)

        # Create columns as vertical boxes
        column_left = QVBoxLayout()
        column_right = QVBoxLayout()

        for g in self.groups:
            if g.column == "left":
                column_left.addLayout(g.buildLayout())
            else:
                column_right.addLayout(g.buildLayout())

        column_left.addStretch()
        column_right.addStretch()

        self.groups_hbox.addLayout(column_left)
        self.groups_hbox.addStretch()
        self.groups_hbox.addLayout(column_right)
        self.groups_hbox.addStretch()

    def aboutDialog(self):
        QMessageBox.about(self, "About Assignment List",
                          "Created by Louie S. - 2023")

    def load_groups(self):
        """
        Load groups data
        """
        # TODO this is debug for now, with fixed values
        self.groups = []
        self.groups.append(Group("test1", "left"))
        self.groups.append(Group("test2", "left"))
        self.groups.append(Group("test3", "right"))
        self.groups.append(Group("test4", "right"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AssignmentList()
    sys.exit(app.exec_())

