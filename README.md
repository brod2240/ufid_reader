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
## Public Course API
### Credit: 
https://github.com/Rolstenhouse/uf_api?tab=readme-ov-file#courses
### How to Use:
**Base URL:**
\[GET\] https://one.ufl.edu/apix/soc/schedule/[parameters] \
Note: term and category are required. lastcontrolnumber is highly suggested \
\
Sample Call (Bare Minimum): \
https://one.ufl.edu/apix/soc/schedule/?category=RES&term=20165 \
\
**Parameters:** \
Appended to the BaseURL as parameter=value1&parameter2=value2 ... \
\
**Semester/Term (Required)** \
term = \[Year(with second digit removed\]\[Semester number\]\[optional Summer Semester\] \
Spring: 1 \
Summer: 5 (Append 6W1 for A. 6W2 for B. 1 for C) \
Fall: 8 \
\
Example: Summer A 2024 would be 22456W1; Fall 2024 would be 2248 \
\
**Program/Category (Required)** \
RES: Campus/Web/Special Program (Regular) (For Summer 2018 and before) \
CWSP: Campus/Web/Special Program (Regular) (Fall 2018 and beyond) \
UFO: UF online program \
IA: Innovation Academy \
HUR: USVI and Puerto Rico \
\
**Number of Results** \
The JSON response from the API includes the last control number, retrieved rows, and total number of rows as of the results as \
\[ \
&nbsp;{ \
&nbsp;&nbsp;"COURSES":[ ], \
&nbsp;&nbsp;"LASTCONTROLNUMBER": \[number\] \
&nbsp;&nbsp;"RETRIEVEDROWS": \[number\] \
&nbsp;&nbsp;"TOTALROWS": \[number\] \
&nbsp;} \
\] \
\
This API limits the number of returned courses. In order to get the next set of results you must set last-control-number= the previous last-control-number. \
\
Example: Using last-control-number=0 along with the required parameters gets you the course results along with LASTCONTROLNUMBER: \[50\], you can then set last-control-number=50 to get the next set of results \
\
**Course Code** \
course-code=eel3135 This parameter lets you pass the course code as a parameter \
\
**Class Number/Section** \
class-num=12345 This parameter lets you pass the class/section number as a parameter \

### Sample Code:
Found in AaronHelpFunc folder 
### Instructions to Run Sample Code 
1. 

## Admin Site (Brianna Version Locally Hosted)
UFID Check In is a web application that allows administrators manage timesheets created when UFIDs are scanned on the raspberry pi, therefore getting a better gage on student attendance. In theory, admins will have an account that gives an overview of students marked present for their courses only. They have the option of filtering through that data to return specific students, dates, section numbers, and course ids to find what they are looking for.
### Features
- Accounts: These keep track of the courses each professor teaches. (Hardcoded,  plan to implement in beta build)
- Course and Section management: Professors have their courses organized for them, in which each course card will display timesheet daata for only that course. (Additional accounts set for creation for beta build)
- Attendance Tracking: Professors can track student attendance, taken from the backend, for all of their courses and section numbers. This application supports filtering of attendance records by date, course number, section number, and student name (plan to change to UFID in beta build). (Implemented for alpha build)
- Responsive design: This application works across different screen devices, though there is room for improvement in layout adaptability. (Implemented for alpha build)

### API Endpoints
- GET/api/professors/int:professor_id/courses: Retrieve courses taught by a specific professor
- GET /api/courses: Get a list of all courses
- GET /api/sections: Get a list of all sections numbers taught
- GET /api/timesheets: Fetch timesheets with optional filters for date, course, section, and student

### Instructions for Admin Site
1. Unzip ufid-web folder
2. In terminal: cd flask-backend
3. enter command: pip install -r requirements.txt
4. cd ../ufid-web
5. enter command: npm install
6. In flask-backend folder, run python app.py
7. In ufid-web folder, run npm start

### Testing
Test plan is provided on how testing was done, including testing API endpoints manually and verifying functionality of search filters and data displalys.
   
## Completed Work
Log of Completed Work: https://docs.google.com/spreadsheets/d/1taW3SdkVjubU3CihEUra0HCIytSY2XjPeqCYWhKH5SU/edit?usp=sharing <br /> <br />
Main Work Completed (Alpha Build):
* Software
   * Created webapp to host database thus emulating UF database and to act as a data manipulation and visualization tool for testing purposes and UI
   * Added table to database for Pi/Kiosk Configuration with the serial number as the primary key and the room the kiosk is in
   * Made a form on webapp to easily add student data to student database for testing
   * Added table to roster page which allows for visualization of student data
   * Wrote program to parse HTML in "dates and deadlines" page of the UF catalog website to find the start and end dates of semesters (located in AaronHelpFunc folder)
   * Wrote program to extract all information given from the public Course API (located in AaronHelpFunc folder)
   * Wrote and tested app routing code for internal get and post methods (including page navigation, form submissions to update database, etc.) as well as external get and post requests so website would act like API
* Hardware
   * 

<br /> <br />
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
Pre-Alpha Project Architecture: https://docs.google.com/document/d/1tP44RrBhFNyO9FV3hFwBYtD2954Nz5rZk2YErq-sL-Y/edit?usp=sharing <br /> <br />
Current Project Architecture: https://docs.google.com/document/d/16P1VVmUHEkcT9Zi2FqWKvdya8piKoZl4C9z6rgN8DTU/edit?usp=sharing <br />
### End Goal Project Architecture:
#### External Interface
Users will interface with a MRD5 scanner and LCD screen. The MRD5 scanner will take in input from either the magnetic stripe of a physical card or the NFC tap of a physical or mobile card. The validation of the ID will be displayed on screen (error, not in roster, present, etc.) along with the name and photo of the student. For admins, teachers, and IT they will interface with a website allowing them to see and manipulate data. 
#### Persistent State
The UF directory and ESODBC data warehouse will be the persistent state in which information such as the student ISO, name, ID number, photo, and class number of enrolled course can be accessed. Another database hosted on a UF server will be used to store the timestamp and Pi/Kiosk configuration data. This server could also host the website. Course data is available in one of the UF servers and can be accessed with a publicly available API. 
#### Internal System
The internal system will use its serial number to send a get request to the database with Pi/Kiosks configurations to get the room it is in. Using the time and room it will send another get request to the course database to find class numbers happening at that time in that room. It will also take in the input of the physical or mobile ID and request information related to the ISO or UFID number. It will then check if the class number of the student match that of the class numbers related to the ID. If the ID is valid it will be timestamped, sent to the database, adn outputted to the LCD. If invalid it will also be outputted with some error message. 
#### Communication Structures
External communication to database with internet connection and API request with data being encrypted. Internal communication between microcontroller and MRD5 scanner with USB and communication between microcontroller and LCD screen with some type of HDMI. 
#### Integrity and Resiliance
Data validation code will be written to ensure that the input is valid with regards to fitting the 8 digit student ID or unique ISO number format. It will also be checked in terms of existing in the student database as stated in the internal system section. Sensitive data will also encrypted before being sent through API requests and requests for sensitive data will need authorized device checked with the serial number of the kiosks in the Pi/Kiosks database. 
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
* Website Form / Web Database Issues   
  * No way to add to data to student database besides hardcoding it or commandline
  * Website form doesn't restrict class data to existing data and allows overwriting which is okay for updating but has the possibility of writing over other students data unitentionally.  
  * ISO is not know by student unless they tap their card or mobile device
    *  Created a form on the new website with the assumption that at the beginning of the year students would manually input there own info
    *  Attempted to use publicly available course API to restrict course/class options though it is not on the whitelist of website allowed on the free version of pythonanywhere
    *  Attempted to get MRD5 scanner reconfigured so that only UFID is received from swipe or tap so ISO is not needed
    *  Now operating under the ideal assumption that student and course data is provided in UF database and will therefore be taken from there instead of provided by students
    *  Using form for testing purposes and easy way to edit data 
* No UF Database Access
  *  Denied UF database access due to FERPA
  *  Switched pseudo-database to be hosted on a pythonanywhere website as closest to ideal solution simulating the UF database servers
  *  Utilized publically available API for courses
  *  Created table in database for student info, RaspPi configurations, and time-stamp data
  *  Inquired UFIT about the type of database (SQL) and what data headings were on the database
* Sockets???
* Internet??
* Threading??  

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
