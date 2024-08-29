'''
import datetime
import requests

# Get the current year
current_year = datetime.datetime.now().year

# Define the academic year ranges
academic_years = [f"{current_year - 1}-{current_year}", f"{current_year}-{current_year + 1}"]

# URL template
url_template = "https://catalog.ufl.edu/UGRD/dates-deadlines/{}/"

# Iterate through academic years and print the URLs
for academic_year in academic_years:
    url = url_template.format(academic_year)

    try:
        response = requests.head(url)
        if response.status_code == 200:
            print(f"URL exists: {url}")
        else:
            print(f"URL does not exist: {url} (Status code: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"Error checking URL: {url} ({e})")
'''

'''
import datetime
import requests
from bs4 import BeautifulSoup

# Get the current year
current_year = datetime.datetime.now().year

# Define the academic year ranges
academic_years = [f"{current_year - 1}-{current_year}", f"{current_year}-{current_year + 1}"]

# URL template
url_template = "https://catalog.ufl.edu/UGRD/dates-deadlines/{}/"

# Function to fetch and parse Classes Begin
def fetch_classes_begin(url, first_year, second_year):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all rows that contain "Classes Begin"
        classes_begin_dates = []
        rows = soup.find_all('tr')

        for row in rows:
            if 'Classes Begin' in row.get_text():
                columns = row.find_all('td')
                if len(columns) > 1:  # Ensure there are enough columns
                    column1_info = columns[1].get_text(strip=True)
                    column2_info = columns[2].get_text(strip=True) if len(columns) > 2 else None
                    
                    # Determine which year to append
                    year = first_year
                    if len(classes_begin_dates) >= 3:  # After the first 3, switch to the second year
                        year = second_year
                    
                    # Append the year to the date information
                    classes_begin_dates.append((f"{column1_info} {year}", f"{column2_info} {year}" if column2_info else None))
        
        return classes_begin_dates
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {url} ({e})")
        return []

# Iterate through academic years and print the URLs and Classes Begin
for academic_year in academic_years:
    url = url_template.format(academic_year)
    print(f"Checking URL: {url}")

    # Check if the URL exists
    try:
        response = requests.head(url)  # Use HEAD to check without downloading the whole page
        if response.status_code == 200:
            print(f"URL exists: {url}")
            # Determine the years based on the academic year
            first_year = academic_year.split('-')[0]
            second_year = academic_year.split('-')[1]

            classes_begin_dates = fetch_classes_begin(url, first_year, second_year)
            print("Classes Begin Dates:")
            for date in classes_begin_dates:
                print(f"Summer A: {date[0]}, Summer C: {date[1] if date[1] else 'N/A'}")
        else:
            print(f"URL does not exist: {url} (Status code: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"Error checking URL: {url} ({e})")
'''

'''
import datetime
import requests
from bs4 import BeautifulSoup
import re

# Get the current year
current_year = datetime.datetime.now().year

# Define the academic year ranges
academic_years = [f"{current_year - 1}-{current_year}", f"{current_year}-{current_year + 1}"]

# URL template
url_template = "https://catalog.ufl.edu/UGRD/dates-deadlines/{}/"

# Function to check if a string is a valid date and return the later date if it's a range
def extract_later_date(date_str):
    # Check for date ranges like "December 7 - 13" or "December 25 - January 2"
    range_match = re.match(r'(\w+ \d{1,2}) - (\w+ \d{1,2}|\d{1,2})', date_str)
    if range_match:
        start_date_str, end_date_str = range_match.groups()
        end_date_str = end_date_str.strip()  # Clean any leading/trailing whitespace
        
        try:
            # Parse start date
            start_date = datetime.datetime.strptime(start_date_str, "%B %d")
            # Check if end_date_str is just a day or a full date
            if end_date_str.isdigit():  # If it's just a day
                end_date = datetime.datetime.strptime(f"{start_date.strftime('%B')} {end_date_str}", "%B %d")
            else:
                # Handle cases like "January 2"
                end_date = datetime.datetime.strptime(end_date_str, "%B %d")
            
            # Return the later date
            return end_date if end_date > start_date else start_date
        except ValueError:
            pass  # If parsing fails, fall through to other checks

    # Check for single dates like "December 7"
    try:
        return datetime.datetime.strptime(date_str, "%B %d")
    except ValueError:
        return None

# Function to fetch and parse Classes Begin, Classes End, and Final Exams
def fetch_classes_dates(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        # Initialize lists to store dates
        classes_begin_dates = []
        classes_end_dates = []
        final_exams_dates = []

        rows = soup.find_all('tr')

        # Parse Classes Begin, Classes End, and Final Exams
        for row in rows:
            # Extract Classes Begin
            if 'Classes Begin' in row.get_text():
                columns = row.find_all('td')
                if len(columns) > 1:  # Ensure there are enough columns
                    column1_info = columns[1].get_text(strip=True)
                    later_date = extract_later_date(column1_info)  # Check if it's a valid date
                    if later_date:  # Only append if it's a valid date
                        classes_begin_dates.append((later_date.strftime("%B %d"), None))  # Append formatted date
                        if len(columns) > 2:
                            column2_info = columns[2].get_text(strip=True)
                            later_date2 = extract_later_date(column2_info)  # Check second column
                            if later_date2:  # Append second column if valid
                                classes_begin_dates[-1] = (later_date.strftime("%B %d"), later_date2.strftime("%B %d"))

            # Extract Classes End
            elif 'Classes End' in row.get_text():
                columns = row.find_all('td')
                if len(columns) > 1:  # Ensure there are enough columns
                    column1_info = columns[1].get_text(strip=True)
                    later_date = extract_later_date(column1_info)  # Check if it's a valid date
                    if later_date:  # Only append if it's a valid date
                        classes_end_dates.append((later_date.strftime("%B %d"), None))  # Append formatted date
                        if len(columns) > 2:
                            column2_info = columns[2].get_text(strip=True)
                            later_date2 = extract_later_date(column2_info)  # Check second column
                            if later_date2:  # Append second column if valid
                                classes_end_dates[-1] = (later_date.strftime("%B %d"), later_date2.strftime("%B %d"))

            # Extract Final Exams
            elif 'Final Exams' in row.get_text():
                columns = row.find_all('td')
                if len(columns) > 1:  # Ensure there are enough columns
                    column1_info = columns[1].get_text(strip=True)
                    later_date = extract_later_date(column1_info)  # Check if it's a valid date
                    if later_date:  # Only append if it's a valid date
                        final_exams_dates.append((later_date.strftime("%B %d"), None))  # Append formatted date
                        if len(columns) > 2:
                            column2_info = columns[2].get_text(strip=True)
                            later_date2 = extract_later_date(column2_info)  # Check second column
                            if later_date2:  # Append second column if valid
                                final_exams_dates[-1] = (later_date.strftime("%B %d"), later_date2.strftime("%B %d"))

        return classes_begin_dates, classes_end_dates, final_exams_dates
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {url} ({e})")
        return [], [], []

# Iterate through academic years and print the URLs and Classes Dates
for academic_year in academic_years:
    url = url_template.format(academic_year)
    print(f"Checking URL: {url}")

    # Check if the URL exists
    try:
        response = requests.head(url)  # Use HEAD to check without downloading the whole page
        if response.status_code == 200:
            print(f"URL exists: {url}")

            classes_begin_dates, classes_end_dates, final_exams_dates = fetch_classes_dates(url)
            
            print("Classes Begin Dates:")
            for begin in classes_begin_dates:
                if begin[1]:  # Only print additional info if it exists
                    print(f" - Summer A Begin: {begin[0]}, Summer C Begin: {begin[1]}")
                else:
                    print(f" - Summer A Begin: {begin[0]}")  # Print only first column info

            print("\nClasses End Dates:")
            for end in classes_end_dates:
                if end[1]:  # Only print additional info if it exists
                    print(f" - Summer A End: {end[0]}, Summer C End: {end[1]}")
                else:
                    print(f" - Summer A End: {end[0]}")  # Print only first column info

            print("\nFinal Exams Dates:")
            for final in final_exams_dates:
                if final[1]:  # Only print additional info if it exists
                    print(f" - Final Exams: {final[0]}, Final Exams (Summer C): {final[1]}")
                else:
                    print(f" - Final Exams: {final[0]}")  # Print only first column info
        else:
            print(f"URL does not exist: {url} (Status code: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"Error checking URL: {url} ({e})")
'''

'''
import datetime
import requests
from bs4 import BeautifulSoup
import re

# Get the current year
current_year = datetime.datetime.now().year

# Define the academic year ranges
academic_years = [f"{current_year - 1}-{current_year}", f"{current_year}-{current_year + 1}"]

# URL template
url_template = "https://catalog.ufl.edu/UGRD/dates-deadlines/{}/"

# Function to check if a string is a valid date and return the later date if it's a range
def extract_later_date(date_str):
    # Check for date ranges like "December 7 - 13" or "December 25 - January 2"
    range_match = re.match(r'(\w+ \d{1,2}) - (\w+ \d{1,2}|\d{1,2})', date_str)
    if range_match:
        start_date_str, end_date_str = range_match.groups()
        end_date_str = end_date_str.strip()  # Clean any leading/trailing whitespace
        
        try:
            # Parse start date
            start_date = datetime.datetime.strptime(start_date_str, "%B %d")
            # Check if end_date_str is just a day or a full date
            if end_date_str.isdigit():  # If it's just a day
                end_date = datetime.datetime.strptime(f"{start_date.strftime('%B')} {end_date_str}", "%B %d")
            else:
                # Handle cases like "January 2"
                end_date = datetime.datetime.strptime(end_date_str, "%B %d")
            
            # Return the later date
            return end_date if end_date > start_date else start_date
        except ValueError:
            pass  # If parsing fails, fall through to other checks

    # Check for single dates like "December 7"
    try:
        return datetime.datetime.strptime(date_str, "%B %d")
    except ValueError:
        return None

# Function to fetch and parse Classes Begin, Classes End, and Final Exams
def fetch_classes_dates(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        # Initialize lists to store dates
        classes_begin_dates = []
        classes_end_dates = []
        final_exams_dates = []

        rows = soup.find_all('tr')

        # Parse Classes Begin, Classes End, and Final Exams
        for row in rows:
            # Extract Classes Begin
            if 'Classes Begin' in row.get_text():
                columns = row.find_all('td')
                if len(columns) > 1:  # Ensure there are enough columns
                    column1_info = columns[1].get_text(strip=True)
                    later_date1 = extract_later_date(column1_info)  # Check if it's a valid date
                    if later_date1:
                        classes_begin_dates.append(later_date1)  # Append as datetime object
                    
                    if len(columns) > 2:
                        column2_info = columns[2].get_text(strip=True)
                        later_date2 = extract_later_date(column2_info)  # Check second column
                        if later_date2:
                            classes_begin_dates.append(later_date2)  # Append as datetime object

            # Extract Classes End
            elif 'Classes End' in row.get_text():
                columns = row.find_all('td')
                if len(columns) > 1:  # Ensure there are enough columns
                    column1_info = columns[1].get_text(strip=True)
                    later_date1 = extract_later_date(column1_info)  # Check if it's a valid date
                    if later_date1:
                        classes_end_dates.append(later_date1)  # Append as datetime object
                    
                    if len(columns) > 2:
                        column2_info = columns[2].get_text(strip=True)
                        later_date2 = extract_later_date(column2_info)  # Check second column
                        if later_date2:
                            classes_end_dates.append(later_date2)  # Append as datetime object

            # Extract Final Exams
            elif 'Final Exams' in row.get_text():
                columns = row.find_all('td')
                if len(columns) > 1:  # Ensure there are enough columns
                    column1_info = columns[1].get_text(strip=True)
                    later_date1 = extract_later_date(column1_info)  # Check if it's a valid date
                    if later_date1:
                        final_exams_dates.append(later_date1)  # Append as datetime object
                    
                    if len(columns) > 2:
                        column2_info = columns[2].get_text(strip=True)
                        later_date2 = extract_later_date(column2_info)  # Check second column
                        if later_date2:
                            final_exams_dates.append(later_date2)  # Append as datetime object

        return classes_begin_dates, classes_end_dates, final_exams_dates
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {url} ({e})")
        return [], [], []

# Function to get the earliest date from a list of dates
def get_earliest_date(dates):
    return min(dates) if dates else None

# Function to get the latest date from a list of dates
def get_latest_date(dates):
    return max(dates) if dates else None

# Iterate through academic years and print the URLs and Classes Dates
for academic_year in academic_years:
    url = url_template.format(academic_year)
    print(f"Checking URL: {url}")

    # Check if the URL exists
    try:
        response = requests.head(url)  # Use HEAD to check without downloading the whole page
        if response.status_code == 200:
            print(f"URL exists: {url}")

            classes_begin_dates, classes_end_dates, final_exams_dates = fetch_classes_dates(url)
            
            print("Classes Begin Dates:")
            if len(classes_begin_dates) >= 7:
                first_three_earliest = get_earliest_date(classes_begin_dates[:3])
                print(f" - Summer 2024 Begin: {first_three_earliest.strftime('%B %d')}")
                print(f" - Fall 2024 Begin: {classes_begin_dates[3].strftime('%B %d')}")
                print(f" - Spring 2025 Begin: {classes_begin_dates[4].strftime('%B %d')}")
                last_two_earliest = get_earliest_date(classes_begin_dates[5:])
                print(f" - Summer 2025 Begin: {last_two_earliest.strftime('%B %d')}")
            else:
                print("Not enough Classes Begin dates found.")

            print("\nClasses End Dates:")
            if len(classes_end_dates) >= 7:
                first_three_latest = get_latest_date(classes_end_dates[:3])
                print(f" - Summer 2024 End: {first_three_latest.strftime('%B %d')}")
                print(f" - Fall 2024 End: {classes_end_dates[3].strftime('%B %d')}")
                print(f" - Spring 2025 End: {classes_end_dates[4].strftime('%B %d')}")
                last_two_latest = get_latest_date(classes_end_dates[5:])
                print(f" - Summer 2025 End: {last_two_latest.strftime('%B %d')}")
            else:
                print("Not enough Classes End dates found.")

            print("\nFinal Exams Dates:")
            for final in final_exams_dates:
                print(f" - Final Exams: {final.strftime('%B %d')}")
        else:
            print(f"URL does not exist: {url} (Status code: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"Error checking URL: {url} ({e})")
'''

'''
import datetime
import requests
from bs4 import BeautifulSoup
import re

# Get the current year
current_year = datetime.datetime.now().year

# Define the academic year ranges
academic_years = [f"{current_year - 1}-{current_year}", f"{current_year}-{current_year + 1}"]

# URL template
url_template = "https://catalog.ufl.edu/UGRD/dates-deadlines/{}/"

# Function to check if a string is a valid date and return the later date if it's a range
# Function to check if a string is a valid date and return the later date if it's a range
def extract_later_date(date_str):
    # Check for date ranges like "December 7 - 13" or "December 25 - January 2"
    range_match = re.match(r'(\w+ \d{1,2}) - (\w+ \d{1,2}|\d{1,2})', date_str)
    if range_match:
        start_date_str, end_date_str = range_match.groups()
        end_date_str = end_date_str.strip()  # Clean any leading/trailing whitespace
        
        try:
            # Parse start date
            start_date = datetime.datetime.strptime(start_date_str, "%B %d")
            # Check if end_date_str is just a day or a full date
            if end_date_str.isdigit():  # If it's just a day
                end_date = datetime.datetime.strptime(f"{start_date.strftime('%B')} {end_date_str}", "%B %d")
            else:
                # Handle cases like "January 2"
                end_date = datetime.datetime.strptime(end_date_str, "%B %d")
            
            # Return the later date
            return end_date if end_date > start_date else start_date
        except ValueError:
            pass  # If parsing fails, fall through to other checks

    # Check for single dates like "December 7"
    try:
        return datetime.datetime.strptime(date_str, "%B %d")
    except ValueError:
        return None
    
def check_dates_in_range(start_dates, end_dates):
    # Get today's date
    today = datetime.datetime.now()

    # Initialize a list to hold the results
    results = []

    # Check each pair of begin and end dates
    for start_date, end_date in zip(start_dates, end_dates):
        # Check if today is on or between the start and end dates
        if start_date <= today <= end_date:
            results.append(True)
        else:
            results.append(False)

    return results

def fetch_classes_dates(url, index):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(response.content, 'html.parser')

        # Initialize lists to store dates
        classes_begin_dates = []
        classes_end_dates = []
        final_exams_dates = []

        rows = soup.find_all('tr')

        # Parse Classes Begin, Classes End, and Final Exams
        for row in rows:
            # Extract Classes Begin
            if 'Classes Begin' in row.get_text():
                columns = row.find_all('td')
                if len(columns) > 1:  # Ensure there are enough columns
                    column1_info = columns[1].get_text(strip=True)
                    later_date1 = extract_later_date(column1_info)  # Check if it's a valid date
                    if later_date1:
                        classes_begin_dates.append(later_date1)  # Append as datetime object
                    
                    if len(columns) > 2:
                        column2_info = columns[2].get_text(strip=True)
                        later_date2 = extract_later_date(column2_info)  # Check second column
                        if later_date2:
                            classes_begin_dates.append(later_date2)  # Append as datetime object

            # Extract Classes End
            elif 'Classes End' in row.get_text():
                columns = row.find_all('td')
                if len(columns) > 1:  # Ensure there are enough columns
                    column1_info = columns[1].get_text(strip=True)
                    later_date1 = extract_later_date(column1_info)  # Check if it's a valid date
                    if later_date1:
                        classes_end_dates.append(later_date1)  # Append as datetime object
                    
                    if len(columns) > 2:
                        column2_info = columns[2].get_text(strip=True)
                        later_date2 = extract_later_date(column2_info)  # Check second column
                        if later_date2:
                            classes_end_dates.append(later_date2)  # Append as datetime object

            # Extract Final Exams
            elif 'Final Exams' in row.get_text():
                columns = row.find_all('td')
                if len(columns) > 1:  # Ensure there are enough columns
                    column1_info = columns[1].get_text(strip=True)
                    later_date1 = extract_later_date(column1_info)  # Check if it's a valid date
                    if later_date1:
                        final_exams_dates.append(later_date1)  # Append as datetime object
                    
                    if len(columns) > 2:
                        column2_info = columns[2].get_text(strip=True)
                        later_date2 = extract_later_date(column2_info)  # Check second column
                        if later_date2:
                            final_exams_dates.append(later_date2)  # Append as datetime object

        # Adjust the list based on the academic year index
        if index == 0:
            classes_begin_dates = classes_begin_dates[-3:]
            classes_end_dates = classes_end_dates[-3:]
            final_exams_dates = final_exams_dates[1:2]  # Adjusted to get a list with one item

            classes_end_dates[0] = final_exams_dates[0] # Replace Spring End date with when Spring Exams finish
        elif index == 1:
            classes_begin_dates = classes_begin_dates[:4]
            classes_end_dates = classes_end_dates[:4]
            final_exams_dates = final_exams_dates[:1]  # Adjusted to get a list with one item

            classes_end_dates[3] = final_exams_dates[0] # Replace Fall End date with when Fall Exams finish

        classes_begin_dates = [date.replace(year=current_year) for date in classes_begin_dates]
        classes_end_dates = [date.replace(year=current_year) for date in classes_end_dates]
        #final_exams_dates = [date.replace(year=current_year) for date in final_exams_dates]

        return classes_begin_dates, classes_end_dates#, final_exams_dates
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {url} ({e})")
        return [], [], []

# Initialize lists to save results from all academic years
all_classes_begin_dates = []
all_classes_end_dates = []
#all_final_exams_dates = []

url_exists = [False, False]

# Iterate through academic years and print the URLs and Classes Dates
for index, academic_year in enumerate(academic_years):
    url = url_template.format(academic_year)
    print(f"Checking URL: {url}")

    # Check if the URL exists
    try:
        response = requests.head(url)  # Use HEAD to check without downloading the whole page
        if response.status_code == 200:
            print(f"URL exists: {url}")
            url_exists[index] = True
            classes_begin_dates, classes_end_dates = fetch_classes_dates(url, index) #, final_exams_dates 

            #print(f" - Spring 2025 End: {classes_end_dates[0]}") #.strftime('%B %d')
            # Append the results to the master lists
            all_classes_begin_dates.extend(classes_begin_dates)
            all_classes_end_dates.extend(classes_end_dates)
            #all_final_exams_dates.append(final_exams_dates)
        else:
            print(f"URL does not exist: {url} (Status code: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"Error checking URL: {url} ({e})")

#2024 - 2023-2024 2024-2025

# Update all_classes_begin_dates and all_classes_end_dates based on URL existence
if url_exists[0] and not url_exists[1]:  # Only the first URL exists
    all_classes_begin_dates = all_classes_begin_dates[0], min(all_classes_begin_dates[-2:])
    all_classes_end_dates = all_classes_end_dates[0],max(all_classes_end_dates[-2:])
    result = check_dates_in_range(all_classes_begin_dates, all_classes_end_dates)
    if result[0] == True: 
        print("1")
    elif result[1] == True:
        print("5")

elif url_exists[1] and not url_exists[0]:  # Only the second URL exists
    all_classes_begin_dates = min(all_classes_begin_dates[:3]), all_classes_begin_dates[3]
    all_classes_end_dates = max(all_classes_end_dates[:3]), all_classes_end_dates[3]
    result = check_dates_in_range(all_classes_begin_dates, all_classes_end_dates)
    if result[0] == True: 
        print("5")
    elif result[1] == True:
        print("8")
elif url_exists[0] and url_exists[1]:  # Both URLs exist
    all_classes_begin_dates = all_classes_begin_dates[0], min(all_classes_begin_dates[1:6]), all_classes_begin_dates[6]
    all_classes_end_dates = all_classes_end_dates[0], max(all_classes_end_dates[1:6]), all_classes_end_dates[6]
    result = check_dates_in_range(all_classes_begin_dates, all_classes_end_dates)
    if result[0] == True: 
        print("1")
    elif result[1] == True:
        print("5")
    elif result[2] == True:
        print("8")
'''


import datetime
import requests
from bs4 import BeautifulSoup
import re

# Get the current year
current_year = datetime.datetime.now().year

# Define the academic year ranges
academic_years = [f"{current_year - 1}-{current_year}", f"{current_year}-{current_year + 1}"]

# URL template
url_template = "https://catalog.ufl.edu/UGRD/dates-deadlines/{}/"

def get_term(suffix):
    modified_year = str(current_year)[0] + str(current_year)[2:]  # Remove the second digit
    return int(modified_year + str(suffix))  # Concatenate the modified year with the suffix

def extract_later_date(date_str):
    range_match = re.match(r'(\w+ \d{1,2}) - (\w+ \d{1,2}|\d{1,2})', date_str)
    if range_match:
        start_date_str, end_date_str = range_match.groups()
        end_date_str = end_date_str.strip()
        
        try:
            start_date = datetime.datetime.strptime(start_date_str, "%B %d")
            if end_date_str.isdigit():
                end_date = datetime.datetime.strptime(f"{start_date.strftime('%B')} {end_date_str}", "%B %d")
            else:
                end_date = datetime.datetime.strptime(end_date_str, "%B %d")
            
            return end_date if end_date > start_date else start_date
        except ValueError:
            pass

    try:
        return datetime.datetime.strptime(date_str, "%B %d")
    except ValueError:
        return None

def check_dates_in_range(start_dates, end_dates):
    today = datetime.datetime.now()
    results = []

    for start_date, end_date in zip(start_dates, end_dates):
        if start_date <= today <= end_date:
            results.append(True)
        else:
            results.append(False)

    return results

def fetch_classes_dates(url, index):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        classes_begin_dates = []
        classes_end_dates = []
        final_exams_dates = []

        rows = soup.find_all('tr')

        for row in rows:
            if 'Classes Begin' in row.get_text():
                columns = row.find_all('td')
                if len(columns) > 1:
                    column1_info = columns[1].get_text(strip=True)
                    later_date1 = extract_later_date(column1_info)
                    if later_date1:
                        classes_begin_dates.append(later_date1)
                    if len(columns) > 2:
                        column2_info = columns[2].get_text(strip=True)
                        later_date2 = extract_later_date(column2_info)
                        if later_date2:
                            classes_begin_dates.append(later_date2)

            elif 'Classes End' in row.get_text():
                columns = row.find_all('td')
                if len(columns) > 1:
                    column1_info = columns[1].get_text(strip=True)
                    later_date1 = extract_later_date(column1_info)
                    if later_date1:
                        classes_end_dates.append(later_date1)
                    if len(columns) > 2:
                        column2_info = columns[2].get_text(strip=True)
                        later_date2 = extract_later_date(column2_info)
                        if later_date2:
                            classes_end_dates.append(later_date2)

            elif 'Final Exams' in row.get_text():
                columns = row.find_all('td')
                if len(columns) > 1:
                    column1_info = columns[1].get_text(strip=True)
                    later_date1 = extract_later_date(column1_info)
                    if later_date1:
                        final_exams_dates.append(later_date1)
                    if len(columns) > 2:
                        column2_info = columns[2].get_text(strip=True)
                        later_date2 = extract_later_date(column2_info)
                        if later_date2:
                            final_exams_dates.append(later_date2)

        if index == 0:
            classes_begin_dates = classes_begin_dates[-3:]
            classes_end_dates = classes_end_dates[-3:]
            final_exams_dates = final_exams_dates[1:2]
            classes_end_dates[0] = final_exams_dates[0]
        elif index == 1:
            classes_begin_dates = classes_begin_dates[:4]
            classes_end_dates = classes_end_dates[:4]
            final_exams_dates = final_exams_dates[:1]
            classes_end_dates[3] = final_exams_dates[0]

        classes_begin_dates = [date.replace(year=current_year) for date in classes_begin_dates]
        classes_end_dates = [date.replace(year=current_year) for date in classes_end_dates]

        return classes_begin_dates, classes_end_dates
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {url} ({e})")
        return [], []

def get_semester(url_exists, all_classes_begin_dates, all_classes_end_dates):
    if url_exists[0] and not url_exists[1]:  # Only the first URL exists
        all_classes_begin_dates = (all_classes_begin_dates[0], min(all_classes_begin_dates[-2:]))
        all_classes_end_dates = (all_classes_end_dates[0], max(all_classes_end_dates[-2:]))
        result = check_dates_in_range(all_classes_begin_dates, all_classes_end_dates)
        if result[0]:
            return 1
        elif result[1]:
            return 5

    elif url_exists[1] and not url_exists[0]:  # Only the second URL exists
        all_classes_begin_dates = (min(all_classes_begin_dates[:3]), all_classes_begin_dates[3])
        all_classes_end_dates = (max(all_classes_end_dates[:3]), all_classes_end_dates[3])
        result = check_dates_in_range(all_classes_begin_dates, all_classes_end_dates)
        if result[0]:
            return 5
        elif result[1]:
            return 8

    elif url_exists[0] and url_exists[1]:  # Both URLs exist
        all_classes_begin_dates = (all_classes_begin_dates[0], min(all_classes_begin_dates[1:6]), all_classes_begin_dates[6])
        all_classes_end_dates = (all_classes_end_dates[0], max(all_classes_end_dates[1:6]), all_classes_end_dates[6])
        result = check_dates_in_range(all_classes_begin_dates, all_classes_end_dates)
        if result[0]:
            return 1
        elif result[1]:
            return 5
        elif result[2]:
            return 8

    return None  # Return None if no conditions are met

# Main logic
def main():
    all_classes_begin_dates = []
    all_classes_end_dates = []
    url_exists = [False, False]

    for index, academic_year in enumerate(academic_years):
        url = url_template.format(academic_year)
        #print(f"Checking URL: {url}")

        try:
            response = requests.head(url)
            if response.status_code == 200:
                #print(f"URL exists: {url}")
                url_exists[index] = True
                classes_begin_dates, classes_end_dates = fetch_classes_dates(url, index)
                all_classes_begin_dates.extend(classes_begin_dates)
                all_classes_end_dates.extend(classes_end_dates)
            #else:
                #print(f"URL does not exist: {url} (Status code: {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"Error checking URL: {url} ({e})")

    # Determine and return the value
    semester = get_semester(url_exists, all_classes_begin_dates, all_classes_end_dates)

    term = get_term(semester)

    # Output the result
    if term is not None:
        return term

if __name__ == "__main__":
    main()
    #print(result)