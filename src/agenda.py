"""An agenda which enables students to keep a record of their task list.

Users may record their tasks and the details of each task. This includes
information about the task title, subject, due date, and completion status.
"""

import json
import sys
from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMainWindow

from setup.add_task_setup import Ui_dialog_new_task
from setup.agenda_setup import Ui_mwindow_agenda


def main() -> None:
    """Opens the agenda window on start-up."""
    app = QtWidgets.QApplication(sys.argv)
    mwindow_agenda = AgendaWindow()
    mwindow_agenda.show()
    sys.exit(app.exec_())


def read_tasks() -> tuple:
    """Reads existing JSON files for lists of tasks.

    Returns:
        task_list: A list of all tasks.
        task_list_hidden: A list of tasks excluding completed tasks.
    """
    with open("resources/task_list.json", "r") as outfile:
        try:
            task_list = json.load(outfile)
            json.dump(task_list, sys.stdout, ensure_ascii=False, indent=4)

            with open("resources/task_list_hidden.json", "r") as outfile_hidden:
                task_list_hidden = json.load(outfile_hidden)
        except ValueError:
            print("Empty JSON file.")
            task_list = []
            task_list_hidden = []

    return task_list, task_list_hidden


class AddTaskDialog(QDialog, Ui_dialog_new_task):
    """Sets up the Add Task dialog window.

    Methods:
        __init__: Inherits the non-functional graphical user interface from
                  the automatically generated code in agenda_setup.py.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)


class AgendaWindow(QMainWindow, Ui_mwindow_agenda):
    """Sets up the Agenda main window.

    Attributes:
        Dialog: Dialog window object for adding a new task.
        hidden_tasks: Completed tasks (may be hidden by the user).
        task_list: List of all tasks.
        task_list_hidden: List of tasks with completed tasks hidden.
    """

    def __init__(self) -> None:
        # Hides completed tasks by default.
        self.Dialog = AddTaskDialog()
        self.hidden_tasks = True
        self.task_list, self.task_list_hidden = read_tasks()
        super().__init__()
        self.setupUi(self)
        self.setStyleSheet(
            """QTableWidget {background-color: transparent;}
            QHeaderView::section {background-color: transparent;}
            QHeaderView {background-color: transparent;}
            QTableCornerButton::section{background-color: transparent;}"""
        )
        self.btn_add_task.clicked.connect(self.open_dialog_add_task)
        self.btn_complete_task.clicked.connect(self.mark_task_complete)
        self.btn_delete_task.clicked.connect(self.delete_task)
        self.btn_hide_completed.clicked.connect(self.hide_completed_tasks)
        self.btn_hide_completed.setText("Show Completed Tasks")
        self.update_list()

    def open_dialog_add_task(self) -> None:
        """Opens the dialog for the user to add a task."""
        self.Dialog.button_box_new_task.accepted.disconnect()
        self.Dialog.button_box_new_task.accepted.connect(self.save_task)

        # Populates the combo box with subject options.
        self.Dialog.comb_box_subject.clear()
        with open("resources/subject_list.txt", "r") as data_file:
            subject_list = data_file.readlines()
            for line in subject_list:
                self.Dialog.comb_box_subject.addItem(line.strip("\n"))
        self.Dialog.open()

    def update_list(self) -> None:
        """Populates the agenda with all tasks."""
        # Displays completed tasks if user selected the option.
        if self.hidden_tasks is True:
            current_list = self.task_list_hidden
        else:
            current_list = self.task_list

        # Creates table to display tasks, resizing to fit content.
        self.table_widget_task_list.setRowCount(len(current_list))
        self.table_widget_task_list.horizontalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeToContents
        )
        self.table_widget_task_list.verticalHeader().setSectionResizeMode(
            QtWidgets.QHeaderView.Fixed
        )

        # Adds tasks to the agenda.
        self.sort_task_list()
        current_row = 0
        for task in current_list:
            current_column = 0
            for task_details in task.values():
                self.table_widget_task_list.setItem(
                    current_row,
                    current_column,
                    QtWidgets.QTableWidgetItem(task_details),
                )
                current_column += 1
            current_row += 1

    def save_task(self) -> None:
        """Saves new tasks to the agenda and JSON file."""
        new_subject = self.Dialog.comb_box_subject.currentText()
        new_due_date = self.Dialog.calendar_due_date.selectedDate().toString(
            "dd/MM/yyyy"
        )
        new_completed = "No"

        # Validates task title input and adds task if validation passed.
        new_task_title = self.Dialog.line_edit_task_title.text()
        if len(new_task_title) <= 30 and len(new_task_title.strip(" ")) > 0:
            task = {
                "task_title": new_task_title,
                "subject": new_subject,
                "due_date": new_due_date,
                "completed": new_completed,
            }
            self.task_list.append(dict(task))
            self.save_task_list()
            self.Dialog.close()
            self.update_list()
        elif len(new_task_title.strip(" ")) == 0:
            self.Dialog.lbl_instruction.setText(
                "You have not entered a task title. Please try again."
            )
        else:
            self.Dialog.lbl_instruction.setText(
                "Your task title exceeds 30 characters. Please try again."
            )

    def save_task_list(self) -> None:
        """Updates the JSON file with the current task list."""
        with open("resources/task_list.json", "w") as outfile:
            json.dump(self.task_list, outfile, ensure_ascii=False, indent=4)

        self.task_list_hidden[:] = [
            task for task in self.task_list if task["completed"] == "No"
        ]
        with open("resources/task_list_hidden.json", "w") as outfile:
            json.dump(self.task_list_hidden, outfile, ensure_ascii=False, indent=4)

    def sort_task_list(self) -> None:
        """Sorts task list by due date."""
        self.task_list.sort(
            key=lambda task: datetime.strptime(task["due_date"], "%d/%m/%Y")
        )
        self.save_task_list()

    def hide_completed_tasks(self) -> None:
        """Hides/shows completed tasks."""
        if self.hidden_tasks is False:
            self.hidden_tasks = True
            self.btn_hide_completed.setText("Show Completed Tasks")
        else:
            self.hidden_tasks = False
            self.btn_hide_completed.setText("Hide Completed Tasks")
        self.update_list()

    def mark_task_complete(self) -> None:
        """Marks selected task as complete/incomplete."""
        selected_row = self.table_widget_task_list.currentRow()
        if self.table_widget_task_list.item(selected_row, 3).text() == "No":
            self.table_widget_task_list.item(selected_row, 3).setText("Yes")
        else:
            self.table_widget_task_list.item(selected_row, 3).setText("No")

        selected_task_title = self.table_widget_task_list.item(selected_row, 0).text()
        selected_subject = self.table_widget_task_list.item(selected_row, 1).text()
        selected_due_date = self.table_widget_task_list.item(selected_row, 2).text()

        # Iterates through task list for matching task and updates completion.
        for num, task in enumerate(self.task_list):
            if (
                task["task_title"] == selected_task_title
                and task["subject"] == selected_subject
                and task["due_date"] == selected_due_date
            ):
                self.task_list[num]["completed"] = self.table_widget_task_list.item(
                    selected_row, 3
                ).text()
        self.save_task_list()
        self.update_list()

    def delete_task(self) -> None:
        """Deletes selected task from agenda."""
        selected_row = self.table_widget_task_list.currentRow()
        selected_task_title = self.table_widget_task_list.item(selected_row, 0).text()
        selected_subject = self.table_widget_task_list.item(selected_row, 1).text()
        selected_due_date = self.table_widget_task_list.item(selected_row, 2).text()

        # Iterates through task list and deletes matching task.
        for task in self.task_list:
            if (
                task["task_title"] == selected_task_title
                and task["subject"] == selected_subject
                and task["due_date"] == selected_due_date
            ):
                self.task_list.remove(task)
        self.save_task_list()
        self.update_list()


if __name__ == "__main__":
    main()
