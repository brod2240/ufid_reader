# UFID Reader
System allows a magnetic stripe/NFC module to read, validate, save, and return student information for attendance purposes.
## Instructions for Kiosk Device Set Up
1. Print [case](https://cad.onshape.com/documents/1842b01a4503db66c32f8896/w/fa3db0597467c5e1710e1e3d/e/0f7033d5ee01bef208a892d8?renderMode=0&uiState=67254f396d5fd65c42971bed) for kiosk. STL file for case can also be found in KioskCase folder (Optional)
2. Connect device to power, to monitor, and to keyboard and mouse as temporary input
3. Install non-graphical raspbian (ONLY FOR RASP PI 4)
4. Connect the device to the internet, either by Wifi or ethernet
5. Connect MRD5 scanner via USB. Make sure to hold power button until the light stops flashing and the device beeps to turn on.
6. Follow the following instructions
## Instructions to Run Code on Device
To run code directly from command line and setup for running from boot:
1. git clone https://github.com/brod2240/ufid_reader.git (within the root directory)
2. cd ufid_reader/UFIDReader
3. bash start
4. The UFID Check-In System is running!

To setup system for running from boot and reboot to test boot functionality:
1. git clone https://github.com/brod2240/ufid_reader.git (within the root directory)
2. cd ufid_reader/UFIDReader
3. bash copy_scripts
4. sudo reboot
5. Once the Pi 4 has rebooted, the UFID Check-In System is running!

Note: If creating your own admin website, make sure to change the base url in the validation code in the first function of ufid_reader/UFIDReader/Packages/Validation/validation.py

## Public Course API
### Credit: 
[Rob Olsthoorn UF API](https://github.com/Rolstenhouse/uf_api?tab=readme-ov-file#courses)
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
**Program/Category (Required)**
RES: Campus/Web/Special Program (Regular) (For Summer 2018 and before) \
CWSP: Campus/Web/Special Program (Regular) (Fall 2018 and beyond) \
UFO: UF online program \
IA: Innovation Academy \
HUR: USVI and Puerto Rico \
\
**Semester/Term (Required)** \
term = \[Year(with second digit removed\]\[Semester number\]\[optional Summer Semester\] \
Spring: 1 \
Summer: 5 (Append 6W1 for A. 6W2 for B. 1 for C) \
Fall: 8 \
\
Example: Summer A 2024 would be 22456W1; Fall 2024 would be 2248 \
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
\
**Meeting Days** \
"day-m": 'true', \
"day-t": 'false', \
"day-w": 'false', \
"day-r": 'false', \
"day-f": 'false', \
"day-s": 'false' \
Note: The days are NOT set as booleans but as strings of 'true' or 'false'. It is supposed to be lowercased. 
\
## API-to-Database.py (UFIDReader/Packages/Validation):
### Instructions
1. Pip install requests if you have not already
2. Run the python file
3. The file will prompt for an input of the semester in the format of year and semester. Input the year without the second digit (e.g 2024 is 224) then the semester (1 for spring, 5 for summer, 8 for fall). For summer A, B, or C you have to append 6W1, 6W2, or 1 respectively to the 5. This is the same way semesters/terms are set in the publicly available course API. (e.g. 2248 for Fall 2024 or 22456W1 for Summer A 2024)
4. The number of sections loaded will be shown as they are loaded in. Once all are loaded in a success message will be shown and a SQL database named courses_{term}.db will be created. A json file will also be created for the use of professor accounts in the professor website.
5. Place the courses_{term}.db in the /data folder for the admin website and place the json file in the professor website

## Gator Check In Site Professor Version (Hosted on PythonAnywhere)
Gator Check In is a web application that allows professors to manage timesheets created when UFIDs are scanned on the raspberry pi, therefore getting a better gage on student attendance. In theory, admins will have an account that gives an overview of students marked present for their courses only. They have the option of filtering through that data to return specific students, dates, section numbers, and course ids to find what they are looking for.
### Features
- Accounts: These keep track of the courses each professor teaches with login authentication
- Course and Section management: Professors have their courses organized for them, in which each course card will display timesheet daata for only that course. (Additional accounts set for creation for beta build)
- Attendance Tracking: Professors can track student attendance, taken from the backend, for all of their courses and section numbers. This application supports filtering of attendance records by date, course number, section number, and student name (plan to change to UFID in beta build). (Implemented for alpha build)
- Responsive design: This application works across different screen devices, though there is room for improvement in layout adaptability. (Implemented for alpha build)

### API Endpoints
BASE: https://brirod2240.pythonanywhere.com/api/
Endpoints: 
        1. /login : authenticates user
        2. /professor/<string:email>/courses : returns the courses taught by the professor with that email
        3. /timesheets : returns all timesheets in db
        4. /timesheets/search : based on filter parameters returns timesheet entries that meet that requirement
        5. /add_timesheet : adds time entry to timesheet table in tb and updates student record
        6. /courses/<course_code>/students : given course code, returns all students in that course
        7. /student/<ufid>/attendance_count : given the student id, return the number of scans made

### Instructions for Professor Site
1. Enter url -> https://brirod2240.pythonanywhere.com/ to browse the website, Beta Build Report has username and password.
2. If you want to recreate this, download ufid_web.zip
3. Extract folder
4. Create python anywhere account
5. Create /web-app folder
6. Place flask_backend and build folder in /web-app folder
7. Reload website tab in Web section of python anywhere
8. Click the link above the tab to look at the website

### Testing
Test plan is provided on how testing was done, including testing API endpoints through unit testing, manual check with Postman, and filter verification.

## Gator Check In Admin Site (Hosted on PythonAnywhere)
GatorUFID or GatorCheck is a web application that allows for database hosting, data manipulation, data visualization, and kiosk configuration. In the validation code hosted on the RaspPi the website is used as an API to verify and save data. For teachers, admins, or IT the website serves to visualize this data in tables, manipulate the data with buttons and forms, and also download data. For the member of this project or for those who want to replicate it the website serves as a tool to easily add test data to the database. 

### Features
- Accounts: Basic admin login capability is implemented with sessions for data security.
- Student Form: Adds or edits student data in student table in roster database.
- Roster Page: Displays student data (UFID, ISO, Name, and Classes) and has Student Form to add more data. Also contains delete buttons for each entry as well as search bar.
- Timesheet Page: Display timesheet data (UFID, ISO, Name, Course, Class, Instructor, Room, and Time). Also contains delete all for debugging purposes and a search bar.
- Kiosks Page: Displays kiosk data (serial number and room number) and ability to add, edit, delete, and search for kiosks.
- Page Navigation

### Website API Endpoints
- GET /kiosks/\[serial_num\]
  - Retrieves room number associated with kiosk
- GET /roster/\[serial_num\]\[ufid or iso\]
  - Retrieves UFID, ISO, first name, last name, and class numbers associated with UFID or ISO
  - Both serial_num and ufid or iso are required to get an actual result
- GET /courses/\[day\]\[roomCode\]
  - Retrieves code, classNumber, instructor(s), meetNo, meetDay, meetTimeBegin, meetTimeEnd, and meetRoomCode associated with that day and room
  - Both day and roomCode are required to get an actual result
  - 'day' can be M, T, W, R, F, or S
  - Ex. roomCode: 'NSC215'
- POST /timesheet\[serial_num\]\[ufid\]\[iso\]\[first_name\]\[first_name\]\[course\]\[class\]\[instructor\]\[room_num\]\[time\]
  - Uses serial_num to verify authorized device by checking it exist in the PiConfig table in the database
  - Saves ufid, iso, first name, last name, course code, class/section number, instructor, room number, and time to timesheet table in database

### Instructions for Admin Site
1. If you want to replicate the app do the following, else if you just want access to the website go to the link https://gatorufid.pythonanywhere.com (to get to admin page use login admin1 for both username and password)
2. Create pythonanywhere account
3. Create webapp and set backend to flask
4. Copy the UFIDWebapp folder into the mysite folder in the file tab (The api and uploads folder can be omitted)
* Structure: 
   * mysite
      * app.py
      * api/
      * data/
      * static/
      * templates/
      * uploads/  
5. Reload the website in the Web tab
6. Click the link above the reload button to open the website  
   
## Completed Work
**Log of Completed Work:** https://docs.google.com/spreadsheets/d/1taW3SdkVjubU3CihEUra0HCIytSY2XjPeqCYWhKH5SU/edit?usp=sharing \
\
**Main Work Completed (Release Candidate and Beta Test)**
* Software
   * Added a prof_profile function to the API-to-Database.py which iterates through the course database and returns a json file structured with the instructors, courses belonging to those instructors, and class sections belonging to those courses.
   * Edited the validate function to incorporate an exam mode. (API calls and Database not created yet)
   * Started encryption for both data at rest (SQL Databases) and in transit (REST API http requests)
   * Created feature that allows users to export timesheet tables to a csv.
   * Started working on faster refresh time of data that prevents users from having to reload the site to see updated scans.
   * Worked on updating backend to allow for custom timsheets title changes for organization purposes.
* Hardware
   * Created a case to house and secure the Rasp Pi 4 and the wires. 
   * Made the Rasp Pi 4 work off boot using an easier to understand github repository.
   * Created easy to use bash scripts to simplify setup on a fresh system.
   * Created setup.py file to verify python version, that pip is installed, and all dependencies are installed. Uses a requirements.txt file which can be added to if required.
   * Formatted GUI and Validation folders as python packages for easy import and use in main.py.

\
**Main Work Completed (Beta Build and Alpha Test):**
* Software
   * Wrote program API-to-Database.py which utilized public course API to get all class sections for that semester and save them to a database
     * Database contains the code, classNumber, instructor(s), meetNo, meetDay, meetTimeBegin, meetTimeEnd, and meetRoomCode
     * Classes were saved using the class section and meeting number as a composite key
     * Allows custom API calls to be made, reducing lag by using new parameters to filter data before returning it
   * Made GET API endpoints for the website to access the student, kiosk, and course data from the kiosk (Details of API endpoints found above)
     * Courses GET endpoint reduces lag previously caused by calling public course API which had a lack of parameters leading to many result being returnned and manually filtered for
   * Made POST API endpoint for the website to save timestamp data from the kiosk to the timesheet table of the database hosted on the website
   * Wrote validation.py code which utilized the new website API endpoints to obtain, validate, save, and return data
   * Added buttons to edit, delete, and delete all kiosks
   * Fixed login to time out after 15 minutes and restrict access to the roster, kiosks, and timesheet page
   * Wrote Unit Tests for the API GET request to the website
   * Wrote a time response test for public course API which analyzed how much time it took to receive and manually filter results given a day parameter. It also provided insight into how many sections and meeting times were loaded and the amount of results given a hardcoded time of 11 AM and a room code of NSC215. Note: No matter what time or room code were used, all meeting times of sections had to be iterated through. 
* Hardware
   * Created functioning system on the Pi 4 which reads a UFID and shows different frames based on program and validation statuses.
     * Uses tkinter to display a user interface.
     * Constantly polls for incoming UFID scan, with four different frames currently: request, loading, success, and failure.
     * Communicates with the database website to determine if an incoming UFID is valid.
     * Performs in an infinite loop, allowing for any number of potential scans without need for recalibration or interaction.
   * Tested Pi 4 core temperature during operation to see if normal use can cause overheating. Exported results to csv for further analysis.
   * Measured the average time the system took for a full iteration, starting at the time a UFID is scanned, and ending when the result frame is displayed. Exported results to csv for further analysis.
   * Adjusted tkinter configuration to allow the display to work correctly on differently sized monitors.

\
**Main Work Completed (Alpha Build):**
* Software
   * Created webapp to host database thus emulating UF database and to act as a data manipulation and visualization tool for testing purposes and UI
   * Added table to database for Pi/Kiosk Configuration with the serial number as the primary key and the room the kiosk is in
   * Made a form on webapp to easily add student data to student database for testing
   * Added table to roster page which allows for visualization of student data
   * Wrote program to parse HTML in "dates and deadlines" page of the UF catalog website to find the start and end dates of semesters (located in AaronHelpFunc folder)
   * Wrote program to extract all information given from the public Course API (located in AaronHelpFunc folder)
   * Wrote and tested app routing code for internal get and post methods (including page navigation, form submissions to update database, etc.) as well as external get and post requests so website would act like API
* Hardware
   * Created Multi-threaded program to handle multiple processes (GUI & Input Validation)
   * Created Parsing thread to take in input from scanner and validate data
   * Wrote GUI thread program to change between interface frame based on input
   * Implemented communication program between parsing thread and GUI thread
   * Modified Raspi4 configuration to work with custontkinter package and display on LCD monitors

\
**Main Work Completed (Design Prototype):**
* Software
   * Changed database over to SQLite. Stores data with UFID or ISO as primary key, student name, and up to 8 courses belonging to student.
   * Updated data validation to reference new pseudo-database
   * Wrote server side socket program to take in 8 digit UFID or 16 digit ISO from client request, validate existance in pseudo-database with data validation code, time-stamp it in csv if valid, and send back a response (either the name character length and name or error character length and the error)
   * Created UI to display validation
* Hardware
   * Switched from Rasp Pi 2040 Microcontroller to Rasp Pi 4B Single-Board-Computer.
   * Solved issue of HID input to be read directly into Rasp Pi 4.
   * Wrote client side socket program to read data, validate that it is 8 or 16 digits, sends request to server side socket, and recieves output from server.

\
**Main Work Completed (Pre-Alpha):**
* Tested barcode scanner. Received unique barcode number as output.
* Tested MRD5 scanner. Received student ID from magnetic stripe and unique ISO from NFC card and mobile tap.
* Tested MRD5 scanner. Received student ID from magnetic stripe and unique ISO from NFC card and mobile tap.
* Created pseudo-database using a csv file populated with ISO number, student ID, name, and class number of enrolled courses.
* Created and Tested data validation of student ID. Prompts for class number which will become an admin function then with each scan checks if the student ID exists and if they are enrolled in the class by checking the class number. 
## Project Architecture
Pre-Alpha Project Architecture: https://docs.google.com/document/d/1tP44RrBhFNyO9FV3hFwBYtD2954Nz5rZk2YErq-sL-Y/edit?usp=sharing <br /> <br />
Alpha Project Architecture: https://docs.google.com/document/d/16P1VVmUHEkcT9Zi2FqWKvdya8piKoZl4C9z6rgN8DTU/edit?usp=sharing <br /> <br />
Current Project Architecture: https://docs.google.com/document/d/1MKxFBsCBQZ5DKFq7oUa7FJucZgOmg5q-gVv8mNC52VA/edit?usp=sharing <br />
### End Goal Project Architecture:
#### External Interface
Users will interface with a MRD5 scanner and LCD screen. The MRD5 scanner will take in input from either the magnetic stripe of a physical card or the NFC tap of a physical or mobile card. The validation of the ID will be displayed on screen (error, not in roster, present, etc.) along with the name and photo of the student. For admins, teachers, and IT they will interface with a website allowing them to see and manipulate data. 
#### Persistent State
The UF directory and ESODBC data warehouse will be the persistent state in which information such as the student ISO, name, ID number, photo, and class number of enrolled course can be accessed. Another database hosted on a UF server will be used to store the timestamp and Pi/Kiosk configuration data. This server could also host the website. Course data is available in one of the UF servers and can be accessed with a publicly available API. 
#### Internal System
The internal system will use its serial number to send a get request to the database with Pi/Kiosks configurations to get the room it is in. Using the time and room it will send another get request to the course database to find class numbers happening at that time in that room. It will also take in the input of the physical or mobile ID and request information related to the ISO or UFID number. It will then check if the class number of the student match that of the class numbers related to the ID. If the ID is valid it will be timestamped, sent to the database, and outputted to the LCD. If invalid it will also be outputted with some error message. 
#### Communication Structures
External communication to database with secure internet connection and API request with data being encrypted. Internal communication between microcontroller and MRD5 scanner with USB and communication between microcontroller and LCD screen with some type of HDMI. 
#### Integrity and Resiliance
Data validation code will be written to ensure that the input is valid with regards to fitting the 8 digit student ID or unique ISO number format. It will also be checked in terms of existing in the student database as stated in the internal system section. Sensitive data will also encrypted before being sent through API requests and requests for sensitive data will need authorized device checked with the serial number of the kiosks in the Pi/Kiosks database. 
## Bugs/Issues
**Full and Detailed List of Bugs/Issues:** https://docs.google.com/document/d/19LEbZKjoLoHLEzeAZ4qlOMeJ4DfzlMnsj3Ypd5segmE/edit?usp=sharing \
\
**Main Bugs/Issues (Release Candidate and Beta Test):**
* Main loop not running
  * Print debugged and found problem to be unresolved error
  * Made sure errors returned response from website and that these responses were translated to the correct validity 0, -1 , -2, -3
* Using real time for validation code seems to not work
  * Print debugged and found to be no problem
  * Rather example tested with was the class section associated with CEN4908C which occurs on Tuesdays and Thursdays and the real-time was a Monday
  * Adding a class section which meets on Monday to a student in the roster database and changing the room associated with the kiosk to the room of the new class that happens on Monday at that time fixes the issue and the student is valid.
* There is no validation for exams
  * Contacted UFIT, Dr. Blanchard, and Carsten to gain knowledge about the system
  * Created the basic structure missing API request to a not yet existing database of exam room reservations
  * Planning to create API request and database for exams
* Case for Rasp Pi too small
  * Made arms holding MRD5 higher so it would fit
  * Made the box wider and longer so the wires would fit
  * Made the wire holes deeper so they wouldn’t need to bend as much
  * Moved the mount holes lower so the SD card on the Rasp Pi would have clearance
* Program which takes course data and sorts it in json file by instructor, course, then section isn’t saving and has duplicates
  * “f” used so that {term} would be recognized as a variable
  * Duplicates removed by using sets instead

\
**Main Bugs/Issues (Beta Build and Alpha Test):**
* Kiosks page can be accessed without login. Note: only temp form page can be seen at time of bug.
  *  Fixed by integrating sessions in Kiosks page app routing
* Sessions not ending after tab or window exited
  *  Fixed using beforeunload listener along with navigation flag
  *  Navigation flag ensures that session is only exited when tab closed and not when page is changed
* Logout button on roster page not displaying properly
  * Fixed with display: inline-block instead of inline
* Kiosk form submit button kicks user out of session
  * Form changed to table and no longer has submit button which kicks users out
* Session kicks out after refreshing twice
  * Session time out after 15 minutes of inactivity instead now not relying on beforeunload listener or navigation flags
* Validation code produces unexpected output sometimes returning an error and other times the UFID, Name, and Validity
  * Fixed by returning the UFID, Name, and Validity each time but with the validity being 0, -1, -2, -3 instead of a boolean. With the errors being converted to a -1, -2, or -3 validity representing serial number not found, UFID or ISO not found, and no matching class, respectively.
* Incorrect output of validation function when cards sequentially scanned
  * Tested validation function for output (Worked as expected)
  * Fixed by clearing input using strip after each scan.
* Lag in validation caused by lack of parameters for public course API
  * Wrote API-to-Database.py program (similar to CourseFetch.py) to take data relating to a semester from the public course API and save it to a database
  * Hosted new course database on website in /data folder

\
**Main Bugs/Issues (Alpha Build):**
* Rasp Pi 4 display resolution too small on monitor
  *  Commandline still appears small but display of the GUI can be adapted to take up the whole screen
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
* Internet
  * Raspi4 disconnects from EDUROAM wifi on startup and does not allow communication with website/database
  * Solution for now is to use ethernet connection to facilitate communication
* Threading
  * GUI thread blocks input from accessing parsing thread
  * Current solution will be to take input directly from USB connection instead of from console  

\
**Main Bugs/Issues (Design Prototype):**
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

\
**Main Bugs/Issues (Pre-Alpha):**
* MRD5 scanner not outputting via HID
  * Fixed by obtaining correctly configured MRD5 scanner.
* No database access
  * In process of obtaining access.
  * Temporarily will configure similar pseudo-database for easy code adaptation when access is granted.
* Cannot read MRD5 scanner data using Pico
  * In process of fixing issue.
