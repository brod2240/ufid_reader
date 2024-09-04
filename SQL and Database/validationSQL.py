import sqlite3
import datetime
import re
import csv

def validate_id(class_number, id_val):
    with sqlite3.connect('StudentCourse2.db') as conn:
        cursor = conn.cursor()
        # Query to find student based on UFID or ISO
        query = '''
        SELECT first_name, last_name, class_number1, class_number2, class_number3, class_number4, 
               class_number5, class_number6, class_number7, class_number8 
        FROM student 
        WHERE UFID = ? OR ISO = ?
        '''
        cursor.execute(query, (id_val, id_val))
        result = cursor.fetchone()
        if result:
            # Check if the class number exists in any of the class number fields
            if class_number in result[2:]:
                return (True, result[0], result[1])
    return (False, '', '')

def validate_course(class_number):
    # Validate the class number format
    if re.match(r'^\d{5}$', class_number):
        return True
    else:
        return False
    
def get_student_name(id_val):
    with sqlite3.connect('StudentCourse2.db') as conn:
        cursor = conn.cursor()
        # Query to find student based on UFID or ISO
        query = '''
        SELECT first_name, last_name
        FROM student 
        WHERE UFID = ? OR ISO = ?
        '''
        cursor.execute(query, (id_val, id_val))
        result = cursor.fetchone()
        if result:
            return result[0] + ' ' + result[1]
        else:
            return ''
        
if __name__ == '__main__':
    while True:
        class_number = input("Enter the class number: ")
        if validate_course(class_number):
            break
        else:
            print("Invalid class number. Please try again.")

    scan = True
    initialScan = {}
    field = ['Time Stamp', 'Student ID', 'Student Name']

    while scan:
        barcode_val = input("Swipe or tap your ID right now: ")
        if re.match(r"^[qQ]$", barcode_val):
            scan = False
        elif re.match(r"^(\d{8}|\d{16})$", barcode_val):
            valid, firstName, lastName = validate_id(class_number, barcode_val)
            if valid:
                currentTime = datetime.datetime.now().strftime("%Y-%m-%d, %I:%M %p")
                print("Valid ID")
                print(f"[{currentTime}] {firstName} {lastName} has been marked as present.")
                initialScan[barcode_val] = (['[' + currentTime + ']', barcode_val, firstName + ' ' + lastName])
            else:
                print("Student not found in class roster or invalid ID. Please try again.")
        else:
            print("Invalid ID. Please try again.")

    # Convert the dictionary values to a list of lists
    finalScans = list(initialScan.values())

    filename = "ufid_barcodes.csv"
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(field)
        csvwriter.writerows(finalScans)

    print("Student attendance updated.")