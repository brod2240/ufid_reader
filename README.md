# UFID Reader
Program to allow a barcode scanner and rfid module to read ufid numbers and output student information for attendance purposes.
## Instructions for Client Host Device Set Up
1. Connect Power, HDMI to monitor, and keyboard (ONLY FOR RASP PI 4)
2. Install non-graphical raspbian (ONLY FOR RASP PI 4)
3. Connect MRD5 scanner via USB. Make sure to hold power button to turn on.
4. Git Pull repository
5. Follow the following instructions
## Instructions to Run Client-Server Communication Between Rasp Pi and Server
1. Ensure the Client.py, Server.py, Data.py, StudentCourse2.db, Validation.py, and ufid_barcodes.csv are all in the same folder.
2. Run Data.py to ensure data is populated in the StudentCourse2.db. To check the database SQLite will have to be downloaded. To add data there is a function called add_student in the Data.py file. 
3. Check the ip address of the server using ipconfig in a commandline on the device hosting the server and change the server ip in the both client.py and server.py file to match.
4. Run Server.py on server host device. Class number used to validate students is hardcoded as this class 27483.
5. Run Client.py on client host device.
6. Scan ID.
## Instructions for GUI
1. Ensure the validationSQL.py and gui.py files are in the same folder.
2. On the command line, ensure you are inside the folder/directory.
3. Run the command 'python gui.py' or 'python3 gui.py' depending on what version of python you have.
4. Enter course id manually (27483)
5. Scan or input id (functionality for manual input implemented only)
6. Manually input 93549135
## Completed Work
Log of Completed Work: https://docs.google.com/spreadsheets/d/1taW3SdkVjubU3CihEUra0HCIytSY2XjPeqCYWhKH5SU/edit?usp=sharing <br /> <br />
Main Work Completed (Design Prototype):
* Software
   * Changed database over to SQLite. Stores data with UFID or ISO as primary key, student name, and up to 8 courses belonging to student.
   * Updated data validation to reference new pseudo-database
   * Wrote server side socket program to take in 8 digit UFID or 16 digit ISO from client request, validate existance in pseudo-database with data validation code, time-stamp it in csv if valid, and send back a response (either the name character length and name or error character length and the error)
   * Created UI to display validation
* Hardware
   * Switched from Rasp Pi 2040 Microcontroller to Rasp Pi 4B Single-Board-Computer.
   * Solved issue of HID input to be read directly into Rasp Pi 4.
   * Wrote client side socket program to read data, validate that it is 8 or 16 digits, sends request to server side socket, and recieves output from server.

<br /> <br />
Main Work Completed (Pre-Alpha):
* Tested barcode scanner. Received unique barcode number as output.
* Tested MRD5 scanner. Received student ID from magnetic stripe and unique ISO from NFC card and mobile tap.
* Tested MRD5 scanner. Received student ID from magnetic stripe and unique ISO from NFC card and mobile tap.
* Created pseudo-database using a csv file populated with ISO number, student ID, name, and class number of enrolled courses.
* Created and Tested data validation of student ID. Prompts for class number which will become an admin function then with each scan checks if the student ID exists and if they are enrolled in the class by checking the class number. 
## Project Architecture
Current Project Architecture: https://docs.google.com/document/d/1tP44RrBhFNyO9FV3hFwBYtD2954Nz5rZk2YErq-sL-Y/edit?usp=sharing <br /> <br />
End Goal Project Architecture:
### External Interface
Users will interface with a MRD5 scanner and LCD screen. The MRD5 scanner will take in input from either the magnetic stripe of a physical card or the NFC tap of a physical or mobile card. The validation of the ID will be displayed on screen (error, not in roster, present, etc.) along with the name and photo of the student. 
Users will interface with a MRD5 scanner and LCD screen. The MRD5 scanner will take in input from either the magnetic stripe of a physical card or the NFC tap of a physical or mobile card. The validation of the ID will be displayed on screen (error, not in roster, present, etc.) along with the name and photo of the student. 
### Persistent State
The UF directory and ESODBC data warehouse will be the persistent state in which information such as the student ISO, name, ID number, photo, and class number of enrolled course can be accessed. Another database will be used to store the timestamp data. 
### Internal System
The internal system will take in the admin input for the class number. It will also take in the input of the physical or mobile ID and request or query the database for information related to the ISO or student ID number. It will then check that the class number which the admin inputs is the same as that related to one of the class numbers related to that ID. If the ID is valid it will be timestamped, sent to the database, and outputted to the LCD. If invalid it will also be outputted with some error message. 
### Communication Structures
External communication to database with TCP/IP. Internal communication between microcontroller and MRD5 scanner with USB and communication between microcontroller and LCD screen to be determined. 
External communication to database with TCP/IP. Internal communication between microcontroller and MRD5 scanner with USB and communication between microcontroller and LCD screen to be determined. 
### Integrity and Resiliance
Data validation code will be written to ensure that the input is valid with regards to fitting the 8 digit student ID or unique ISO number format. It will also be checked in terms of existing in the class roster as stated in the interal systems section.
## Bugs/Issues
Full and Detailed List of Bugs/Issues: https://docs.google.com/document/d/19LEbZKjoLoHLEzeAZ4qlOMeJ4DfzlMnsj3Ypd5segmE/edit?usp=sharing <br /> <br />
Main Bugs/Issues (Alpha Build):
* Rasp Pi 4 display resolution too small on monitor
  * Commandline still appears small but display of the GUI can be adapted to take up the whole screen
* Publicly available course API has inaccurate information with regards to the total rows returned
  *  Fixed by receiving data until all was there was no more
* Publicly available course API not on whitelist of website on free version of pythonanywhere so it doesn't work
  *  Running course API on RaspPi instead of website
  *  Also, is closer to ideal design where everything but the databases are on the RaspPi and to get info the RaspPi is making API request to the website or course API
* Course API needs year and semester to obtain course data for the desired semester
  *  Programmed a HTML parser to parse for start and end dates from the academic calendar
  *  First used on website but did not work due to whitelist of websites
  *  Likely reutilized now that access to course API can be done from RaspPi      
* Lacking permanent hosting and effient way to visualize and edit data
  *  Created website on pythonanywhere to host database and easily manipulate and visualize data  
* No way to add to data to student database besides hardcoding it or commandline
  *  Created a form on the new website with the assumption that at the beginning of the year students would manually input there own info
  *  Now operating under the ideal assumption that data is provided in UF database and will therefore be taken from there instead of provided by students
  *  Using form for testing purposes and easy way to edit data
* Website form doesn't restrict class data to existing data and allows overwriting which is okay for updating but has the possibility of writing over other students data unitentionally.
  *  Attempted to use publicly available course API to restrict options though it is not on the whitelist of website allowed on the free version of pythonanywhere
  *  Operating under the ideal assumption that data is provided in UF database and will therefore be taken from there instead of provided by students
  *  Using form for testing purposes and easy way to edit data      
* No Database Access
  *  Denied UF database access due to FERPA
  *  Switched pseudo-database to be hosted on a pythonanywhere website as closest to ideal solution simulating the UF database servers
  *  Utilized publically available API for courses
  *  Created table in database for student info, RaspPi configurations, and time-stamp data
  *  Inquired UFIT about the type of database (SQL) and what data headings were on the database

<br /> <br />
Main Bugs/Issues (Design Prototype):
* Rasp Pi 4 display resolution too small on monitor
  * Kept the same for now 
* Reading HID data from MRD5 scanner directly not working
  * Switched from Rasp Pi 2040 to Rasp Pi 4
  * Used python input() function
* Client-Server communication between Rasp Pi 4 and Server device via TCP/IP using sockets
  *  Switched port number
  *  Used ipconfig command on server device to set ip address for connection
* No Database Access
  *  Denied UF database access due to FERPA
  *  Switched from using csv pseudo-database to SQLite pseudo-database hosted on a server device
  *  Created csv for time-stamp data hosted on server device
  *  Attempt to get indirect access to the database structure
  *  Attempt to host server on CISE server
* GUI connection to Rasp Pi 4
  * Fixed using python tkinter

<br /> <br />
Main Bugs/Issues (Pre-Alpha):
* MRD5 scanner not outputting via HID
  * Fixed by obtaining correctly configured MRD5 scanner.
* No database access
  * In process of obtaining access.
  * Temporarily will configure similar pseudo-database for easy code adaptation when access is granted.
* Cannot read MRD5 scanner data using Pico
  * In process of fixing issue.
