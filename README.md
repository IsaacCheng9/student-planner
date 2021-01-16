# student-planner
A student planner which includes an agenda, and a timetable to help students
organise their work.

## Getting Started
These instructions will help you to get the software for this student planner
running on your computer.

### Prerequisites
Python 3.7.0 or later is required for this software to run. It can be installed
from [Python's website here.](https://www.python.org/getit/)

### Installing
The following Python module must be installed, as it is not built into the
Python installation by default:
- pyqt5 [for user interfaces]
```
pip install pyqt5
```

## Instructions
You can run the student planner by running `student_planner.py`, which will
provide you with a main menu for the application.

## Other Details

### Code Style
This project was developed using Python's
[PEP 8 style guide for code](https://www.python.org/dev/peps/pep-0008/), as it
is a commonly used standard within the Python community.

### Tools Used
[Qt Creator](https://www.qt.io/download) was used to design the user interfaces
for this project in a what you see is what you get (WYSIWYG) editor.

PyQt5's
[pyuic5](https://www.riverbankcomputing.com/static/Docs/PyQt5/designer.html)
was used to generate the base Python code from the user interface designs,
effectively converting the `.ui` files to `.py` files. These generated code
files were marked with the `_setup.py` suffixes, and they were imported into
the other Python files so that functionality could be developed for the user
interface objects. 