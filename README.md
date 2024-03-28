# ufid_reader
Program to allow a barcode scanner and rfid module to read ufid numbers and output student information for attendance purposes
# Completed Work
Log of Completed Work: https://docs.google.com/spreadsheets/d/1taW3SdkVjubU3CihEUra0HCIytSY2XjPeqCYWhKH5SU/edit?usp=sharing
* Tested barcode scanner. Received unique barcode number as output
* Tested MDR5 scanner. Received student ID from magnetic stripe and unique ISO from NFC card and mobile tap
* Created pseudo-database using a csv file populated with ISO number, student ID, name, and class number of enrolled courses.
* Created and Tested data validation of student ID. Prompts for class number which will become an admin function then with each scan checks if the student ID exists and if they are enrolled in the class by checking the class number. 
# Project Architecture
# Bugs
