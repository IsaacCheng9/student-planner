""" A student planner which includes an agenda and a timetable.

Users may use the agenda to keep a record of their task list, and they may use
the timetable to keep track of their lesson schedule.
"""

import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

from student_planner_setup import Ui_mwindow_menu
from agenda import AgendaWindow
from timetable import TimetableWindow
from my_subjects import MySubjectsWindow


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    mwindow_menu = MainMenuWindow()
    mwindow_menu.show()
    sys.exit(app.exec_())


class MainMenuWindow(QMainWindow, Ui_mwindow_menu):
    """Sets up the main menu window."""

    def __init__(self) -> None:
        self.mwindow_my_subjects = MySubjectsWindow()
        self.mwindow_agenda = AgendaWindow()
        self.mwindow_timetable = TimetableWindow()
        super().__init__()
        self.setupUi(self)

        self.btn_my_subjects.clicked.connect(self.open_mwindow_my_subjects)
        self.btn_agenda.clicked.connect(self.open_mwindow_agenda)
        self.btn_timetable.clicked.connect(self.open_mwindow_timetable)

    def open_mwindow_my_subjects(self) -> None:
        """Opens the main window for My Subjects."""
        self.mwindow_my_subjects.show()

    def open_mwindow_agenda(self) -> None:
        """Opens the main window for Agenda."""
        self.mwindow_agenda.show()

    def open_mwindow_timetable(self) -> None:
        """Opens the main window for Timetable."""
        self.mwindow_timetable.show()


if __name__ == "__main__":
    main()
