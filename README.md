# UFID Reader
Program to allow a barcode scanner and rfid module to read ufid numbers and output student information for attendance purposes
## Completed Work
Log of Completed Work: https://docs.google.com/spreadsheets/d/1taW3SdkVjubU3CihEUra0HCIytSY2XjPeqCYWhKH5SU/edit?usp=sharing
Main Work Completed:
* Tested barcode scanner. Received unique barcode number as output.
* Tested MDR5 scanner. Received student ID from magnetic stripe and unique ISO from NFC card and mobile tap.
* Created pseudo-database using a csv file populated with ISO number, student ID, name, and class number of enrolled courses.
* Created and Tested data validation of student ID. Prompts for class number which will become an admin function then with each scan checks if the student ID exists and if they are enrolled in the class by checking the class number. 
## Project Architecture
Current Project Architecture: https://docs.google.com/document/d/1tP44RrBhFNyO9FV3hFwBYtD2954Nz5rZk2YErq-sL-Y/edit?usp=sharing
### External Interface
Users will interface with a MDR5 scanner and LCD screen. The MDR5 scanner will take in input from either the magnetic stripe of a physical card or the NFC tap of a physical or mobile card. The validation of the ID will be displayed on screen (error, not in roster, present, etc.) along with the name and photo of the student. 
### Persistent State
The UF directory and ESODBC data warehouse will be the persistent state in which information such as the student ISO, name, ID number, photo, and class number of enrolled course can be accessed. Another database will be used to store the timestamp data. 
### Internal System
The internal system will take in the admin input for the class number. It will also take in the input of the physical or mobile ID and request or query the database for information related to the ISO or student ID number. It will then check that the class number which the admin inputs is the same as that related to one of the class numbers related to that ID. If the ID is valid it will be timestamped, sent to the database, and outputted to the LCD. If invalid it will also be outputted with some error message. 
### Communication Structures
External communication to database with TCP/IP. Internal communication between microcontroller and MDR5 scanner with USB and communication between microcontroller and LCD screen to be determined. 
### Integrity and Resiliance
Data validation code will be written to ensure that the input is valid with regards to fitting the 8 digit student ID or unique ISO number format. It will also be checked in terms of existing in the class roster as stated in the interal systems section
## Bugs/Issues
Full and Detailed List of Bugs/Issues: https://docs.google.com/document/d/19LEbZKjoLoHLEzeAZ4qlOMeJ4DfzlMnsj3Ypd5segmE/edit?usp=sharing <br />
Main Bugs/Issues:
* MDR5 scanner not outputting via HID
  * Fixed by obtaining correctly configure MDR5 scanner
* No database access
  * In process of obtaining access
  * Temporarily will configure similar pseudo-database for easy code adaptation when access is granted
* Cannot read MDR5 scanner data using Pico
  * In process of fixing issue
