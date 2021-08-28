"""A timetable which enables students to keep track of their lesson schedule.

Users may enter the subject, teacher, and room for each timetable slot.
"""

import json
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMainWindow

from setup.edit_timetable_setup import Ui_dialog_edit_timetable
from setup.timetable_setup import Ui_mwindow_timetable


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    mwindow_timetable = TimetableWindow()
    mwindow_timetable.show()
    sys.exit(app.exec_())


def read_lessons() -> list:
    """Reads JSON files for list of lessons to display in timetable.

    Returns:
        timetable: A list of lessons in the timetable.
    """
    with open("resources/timetable.json", "r") as outfile:
        try:
            timetable = json.load(outfile)
        except ValueError:
            print("Empty JSON file.")
            timetable = []

        # Adds empty dictionary values for empty timetable slots.
        missing_lessons = 25 - len(timetable)
        for index in range(missing_lessons):
            lesson = {"subject": " ", "teacher": " ", "room": " "}
            timetable.append(lesson)

    return timetable


class EditTimetableDialog(QDialog, Ui_dialog_edit_timetable):
    """Sets up the Edit Timetable dialog."""

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)


class TimetableWindow(QMainWindow, Ui_mwindow_timetable):
    """Sets up the Timetable main window.

    Attributes:
        Dialog: Dialog window for editing a timetable slot.
        timetable: List of lessons in the timetable.
    """

    def __init__(self) -> None:
        super().__init__()
        self.Dialog = EditTimetableDialog()
        self.timetable = read_lessons()
        self.setupUi(self)
        self.setStyleSheet(
            """QTableWidget {background-color: transparent;}
            QHeaderView::section {background-color: transparent;}
            QHeaderView {background-color: transparent;}
            QTableCornerButton::section{background-color: transparent;}"""
        )
        self.btn_edit_timetable.clicked.connect(self.open_dialog_edit_timetable)
        self.btn_clear_timetable.clicked.connect(self.clear_timetable_slot)
        self.update_timetable()

    def open_dialog_edit_timetable(self) -> None:
        """Opens the dialog window for editing the timetable."""
        self.Dialog.button_box_edit_timetable.accepted.disconnect()
        self.Dialog.button_box_edit_timetable.accepted.connect(self.save_lesson)

        # Populates the combo box with subject options.
        with open("resources/subject_list.txt", "r") as data_file:
            self.Dialog.comb_box_subject.clear()
            subject_list = data_file.readlines()
            for line in subject_list:
                self.Dialog.comb_box_subject.addItem(line.strip("\n"))
        self.Dialog.open()

    def update_timetable(self) -> None:
        """Populates the timetable with all lessons."""
        # Resizes columns and rows to fit the contents.
        self.table_widget_timetable.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )
        self.table_widget_timetable.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )

        # Adds lesson details to each cell in the timetable.
        for row_index, row in enumerate(self.timetable[::5]):
            for column_index, column in enumerate(range(5)):
                index = (row_index * 5) + column_index
                lesson_details = (
                    (self.timetable[index]["subject"])
                    + "\n"
                    + (self.timetable[index]["teacher"])
                    + "\n"
                    + (self.timetable[index]["room"])
                )
                self.table_widget_timetable.setItem(
                    row_index, column_index, QtWidgets.QTableWidgetItem(lesson_details)
                )

    def save_timetable_list(self) -> None:
        """Updates the JSON file with the current timetable list."""
        with open("resources/timetable.json", "w") as outfile:
            json.dump(self.timetable, outfile, ensure_ascii=False, indent=4)
        self.update_timetable()

    def save_lesson(self) -> None:
        """Saves the lesson to the selected timetable slot."""
        selected_row = self.table_widget_timetable.currentRow()
        selected_column = self.table_widget_timetable.currentColumn()
        lesson_subject = self.Dialog.comb_box_subject.currentText()
        lesson_teacher = self.Dialog.line_edit_teacher.text()
        lesson_room = self.Dialog.line_edit_room.text()

        # Saves lesson to selected timetable slot if length validations passed.
        if len(lesson_teacher) > 30:
            self.Dialog.lbl_instruction.setText(
                "Your teacher input exceeds 30 characters. Please try again."
            )
        elif len(lesson_room) > 20:
            self.Dialog.lbl_instruction.setText(
                "Your room input exceeds 30 characters. Please try again."
            )
        else:
            lesson = {
                "subject": lesson_subject,
                "teacher": lesson_teacher,
                "room": lesson_room,
            }
            index = (selected_row * 5) + selected_column
            self.timetable[index] = lesson
            self.save_timetable_list()
            self.Dialog.close()

    # Clears the lesson from the selected timetable slot.
    def clear_timetable_slot(self) -> None:
        selected_row = self.table_widget_timetable.currentRow()
        selected_column = self.table_widget_timetable.currentColumn()

        # Removes the lesson details from the timetable slot.
        lesson = {"subject": "", "teacher": "", "room": ""}
        index = (selected_row * 5) + selected_column
        self.timetable[index] = lesson
        self.save_timetable_list()


# Opens the main window when the program is executed.
if __name__ == "__main__":
    main()
