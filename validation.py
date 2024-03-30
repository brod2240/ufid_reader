import csv
import datetime
import re

def validate_id(class_number, id_val, filename='UFIDProjectSampleDatabase.csv'):
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if (id_val == row[0] or id_val == row[1]):
                class_numbers = row[4].split()
                if class_number in class_numbers:
                    return (True, row[2], row[3])
    return (False, '', '')

if __name__ == '__main__':

    filename = "ufid_barcodes.csv"

    initialScan = {}

    field = ['Time Stamp', 'Student ID', 'Student Name']

    while True: 
        class_number = input("Enter the class number: ")
        if re.match(r'^\d{5}$', class_number):
            break
        else:
            print("Invalid class number. Please try again.")

    scan = True

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
                initialScan[barcode_val] =(['[' + currentTime + ']', barcode_val, firstName + ' ' + lastName])
            else:
                print("Student not found in class roster or invalid ID. Please try again.")
        else:
            print("Invalid ID. Please try again.")
        
    
    # Convert the dictionary values to a list of lists for writing to CSV
    finalScans = list(initialScan.values())

    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(field)
        csvwriter.writerows(finalScans)

    print("Student attendance updated.")
