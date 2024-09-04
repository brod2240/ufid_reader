import csv

if __name__ == '__main__':

    filename = "ufid_barcodes.csv"

    barcodes = []

    field = ['Barcode Value']

    scan = True

    while scan:
        barcode_val = input("Scan a barcode right now: ")
        if (barcode_val == ''):
            scan = False
        else:
            barcodes.append([barcode_val])
        
    
    with open(filename, 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(field)
        csvwriter.writerows(barcodes)

    print("Barcodes Stored")
