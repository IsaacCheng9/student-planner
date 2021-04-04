"""A subject list which enables students to add subjects to dropdown menus."""

import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QMainWindow

from src.setup.add_subject_setup import Ui_dialog_new_subject
from src.setup.my_subjects_setup import Ui_mwindow_my_subjects


def main() -> None:
    app = QtWidgets.QApplication(sys.argv)
    mwindow_my_subjects = MySubjectsWindow()
    mwindow_my_subjects.show()
    sys.exit(app.exec_())


class AddSubjectDialog(QDialog, Ui_dialog_new_subject):
    """Sets up the Add Subject dialog."""

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)


def sort_subject_list() -> None:
    """Sorts the subject list text file alphanumerically."""
    with open("resources/subject_list.txt", "r+") as outfile:
        lines = outfile.readlines()
        lines.sort()


class MySubjectsWindow(QMainWindow, Ui_mwindow_my_subjects):
    """Sets up the My Subjects main window.

    Attributes:
        Dialog: Dialog window for adding new subjects.
    """

    def __init__(self) -> None:
        super().__init__()
        self.Dialog = AddSubjectDialog()
        self.setupUi(self)

        self.btn_add_subject.clicked.connect(self.open_dialog_add_subject)
        self.btn_delete_subject.clicked.connect(self.delete_subject)

        # Populates the list widget on window startup.
        with open("resources/subject_list.txt", "r") as data_file:
            subject_list = data_file.readlines()
            print(subject_list)
            print(len(subject_list))
            for line in subject_list:
                self.list_widget_my_subjects.addItem(line.strip("\n"))
            self.list_widget_my_subjects.sortItems()
            sort_subject_list()

    def open_dialog_add_subject(self) -> None:
        """Opens the dialog window for the user to add a subject."""
        self.Dialog.button_box_new_subject.accepted.disconnect()
        self.Dialog.button_box_new_subject.accepted.connect(self.save_subject)
        self.Dialog.open()

    def delete_subject(self) -> None:
        """Deletes the selected subject."""
        selected_item = self.list_widget_my_subjects.selectedItems()
        for item in selected_item:
            self.list_widget_my_subjects.takeItem(
                self.list_widget_my_subjects.row(item))
        self.save_subject_list()

    def save_subject_list(self) -> None:
        """Saves the subject list."""
        with open("resources/subject_list.txt", "w") as outfile:
            for i in range(self.list_widget_my_subjects.count()):
                subject = self.list_widget_my_subjects.item(i).text()
                outfile.write(subject + "\n")

    def save_subject(self) -> None:
        """Saves input to a .txt file for the list of subjects."""
        new_subject_name = self.Dialog.line_edit_subject_name.text()
        if len(new_subject_name) <= 30 and len(
                new_subject_name.strip(" ")) > 0:
            print(new_subject_name)
            self.list_widget_my_subjects.addItem(new_subject_name)
            self.list_widget_my_subjects.sortItems()
            with open("resources/subject_list.txt", "a") as outfile:
                outfile.write(new_subject_name + "\n")
            sort_subject_list()
            self.Dialog.close()
        elif len(new_subject_name.strip(" ")) == 0:
            self.Dialog.lbl_instruction.setText(
                "You have not entered a subject name. Please try again.")
        else:
            self.Dialog.lbl_instruction.setText(
                "Your subject name exceeds 30 characters. Please try again.")


if __name__ == "__main__":
    main()
