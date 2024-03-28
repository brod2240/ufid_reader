import csv
import datetime

def validate_id(class_number, id_val, filename='UFIDProjectSampleDatabase.csv'):
    with open(filename, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if (barcode_val == row[0] or barcode_val == row[1]):
                class_numbers = row[4].split()
                if class_number in class_numbers:
                    return (True, row[2], row[3])
    return (False, '', '')

if __name__ == '__main__':

    filename = "ufid_barcodes.csv"

    barcodes = []

    field = ['Barcode Value']

    class_number = input("Enter the class number: ")

    scan = True

    while scan:
        barcode_val = input("Scan a barcode right now: ")
        if (barcode_val == ''):
            scan = False
        else:
            valid, firstName, lastName = validate_id(class_number, barcode_val)
            if valid:
                currentTime = datetime.datetime.now().strftime("%Y-%m-%d, %I:%M %p")
                print("Valid ID")
                print(f"[{currentTime}] {firstName} {lastName} has been marked as present.")
                barcodes.append([barcode_val])
            else:
                print("Invalid ID. Please try again.")
        
    
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(field)
        csvwriter.writerows(barcodes)

    print("Barcodes Stored.")
