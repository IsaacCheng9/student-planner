# student-planner

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A desktop application developed in Python with PyQt5 to help students organise
their work in a student planner consisting of an agenda and a timetable.

## Installation

These instructions will help you to get the software for this student planner
running on your computer.

### Python Version

Python 3.7.0 or later is required for this software to run. It can be installed
from [Python's website here.](https://www.python.org/getit/)

### Python Libraries

The following Python library must be installed, as it is not built into the
Python installation by default:

- pyqt5 [for user interfaces]

```
pip install pyqt5
```

## Usage

You can run the student planner by running `student_planner.py`, which will
provide you with a main menu for the application.

### Main Menu

The main menu helps you to navigate across the parts of the student planner,
which includes My Subjects, Agenda, and Timetable.

### My Subjects

This enables you to enter the subjects which you are studying. These will appear
in the dropdown menus in other parts of the application to select the relevant
subject.

### Agenda

In the agenda, you can enter tasks which you must complete in the future. This
includes the task title, subject, and due date for the task.

### Timetable

The timetable helps you to organise your weekly schedule by editing a 5x5 grid,
which represents five hourly slots across the weekdays. In this grid, each cell
can be edited to add a subject, teacher, and room for that hour.

## Tools Used

[Qt Creator](https://www.qt.io/download) was used to design the user interfaces
for this project in a what you see is what you get (WYSIWYG) editor.

PyQt5's
[pyuic5](https://www.riverbankcomputing.com/static/Docs/PyQt5/designer.html)
was used to generate the base Python code from the user interface designs,
effectively converting the `.ui` files to `.py` files. These generated code
files were marked with the `_setup.py` suffixes, and they were imported into the
other Python files so that functionality could be developed for the user
interface objects. 