Overview

The Habit Tracker application is designed to help users track their daily and weekly habits, monitor streaks, and analyze their habit completion patterns. The application includes a graphical user interface (GUI) built using the Tkinter library in Python. The core functionality is implemented in the habit_tracker.py script, and the GUI is implemented in the habit_tracker_gui.py script. Additionally, there are unit tests in the test_habit_tracker.py script to ensure the correct behavior of the core functionality.


Table of Contents

1. Dependencies
2. Installation
3. Usage
4. Features
5. Graphical User Interface
6. File Management
7. Testing


Dependencies

Python Version: Python 3.3 or higher
Tkinter: The GUI is built using the Tkinter library, which is included in standard Python installations.
json: The application uses the JSON module for reading and writing habit data to a file.
os: The os module is used for file-related operations.
datetime: The datetime module is utilized for working with dates and times.
unittest: The unittest module is used for writing and executing unit tests.


Installation

 1.Clone the repository to your local machine. 
 git clone:  https://github.com/Ashmi11/Habit-tracker-application-using-python 

2.Navigate to the project directory:
cd habit-tracker

3.Install the required dependencies:
pip install -r requirements.txt


Usage

Launch the GUI application with:
python habit_tracker_gui.py


Features

 Create Habit: Add new habits with specified names and periodicities.

 Delete Habit: Remove existing habits based on their names.

 Complete Task: Mark a habit as completed, incrementing its streak.

 Streak Analytics: Retrieve streak information for individual habits or the longest streak across all habits.

 Periodicity Filtering: List habits based on their periodicity (daily or weekly).

Broken Habits Detection: Identify habits with streaks broken due to non-completion.



Graphical User Interface

The graphical user interface (GUI) offers a more user-friendly experience for habit 
tracking. It includes tabs for creating habits, deleting habits, completing tasks, 
viewing streaks, listing habits, and accessing analytics.


File Management

Data File: The application uses a JSON data file (habit_data.json) to persistently store habit information. This file is created in the same directory as the scripts.

Loading Data: Existing habit data is loaded when the HabitTracker class is instantiated.

Saving Data: The save_data method writes the current habit data back to the JSON file.

Resetting Data: The reset_data method clears all habit data and saves the empty list back to the JSON file.


Testing

The test_habit_tracker.py script contains a suite of unit tests. Run the tests with:
python test_habit_tracker.py

The test data should be modifies according to the time it is being carried out to ensure accurate results.
For example, the test case for broken habits requires that only one habit is broken for test to pass, so the simulation of completed time for habits should be adjusted accordingly.

Note: 

Ensure that the habit_tracker.py script is in the same directory as habit_tracker_gui.py and test_habit_tracker.py for the GUI and unit tests to work correctly.

This documentation provides an overview of the application's functionality and usage. For detailed information about the classes and methods, refer to the comments and docstrings in the source code.





