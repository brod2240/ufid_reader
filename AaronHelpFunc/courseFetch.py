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

def after_end_dates(end_dates):
    today = datetime.datetime.now()
    results = []
    for end_date in end_dates:
        if today > end_date:
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
        after_result = after_end_dates(all_classes_end_dates)
        if result[0] or (not after_result[0] and not after_result[1]):
            return 1
        elif result[1] or (after_result[0] and not after_result[1]):
            return 5
        else:
            return 8


    elif url_exists[1] and not url_exists[0]:  # Only the second URL exists
        all_classes_begin_dates = (min(all_classes_begin_dates[:3]), all_classes_begin_dates[3])
        all_classes_end_dates = (max(all_classes_end_dates[:3]), all_classes_end_dates[3])
        result = check_dates_in_range(all_classes_begin_dates, all_classes_end_dates)
        after_result = after_end_dates(all_classes_end_dates)
        if result[0] or (not after_result[0] and not after_result[1]):
            return 5
        elif result[1] or (after_result[0] and not after_result[1]):
            return 8
        else:
            return 8

    elif url_exists[0] and url_exists[1]:  # Both URLs exist
        all_classes_begin_dates = (all_classes_begin_dates[0], min(all_classes_begin_dates[1:6]), all_classes_begin_dates[6])
        all_classes_end_dates = (all_classes_end_dates[0], max(all_classes_end_dates[1:6]), all_classes_end_dates[6])
        result = check_dates_in_range(all_classes_begin_dates, all_classes_end_dates)
        after_result = after_end_dates(all_classes_end_dates)
        if result[0] or (not after_result[0] and not after_result[1] and not after_result[2]):
            return 1
        elif result[1] or (after_result[0] and not after_result[1] and not after_result[2]):
            return 5
        elif result[2] or (after_result[0] and after_result[1]):
            return 8


    return None  # Return None if no conditions are met # Change to 1 5 or 8 so it doesn't break

# Main logic
def get_term():
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

    modified_year = str(current_year)[0] + str(current_year)[2:]  # Remove the second digit
    return int(modified_year + str(semester))  # Concatenate the modified year with the suffix

def fetch_courses(course_code=None, class_num=None):
    # URL to send the GET request to
    url = "https://one.ufl.edu/apix/soc/schedule/"

    term = get_term()

    # Initialize query parameters
    params = {
        "category": "CWSP",
        "term": term,  # Adjusted to the term you specified 6W1 for A. 6W2 for B. 1 for C
        "last-control-number": 0
    }

    # Add course_code and class_num to params if provided
    if course_code:
        params["course-code"] = course_code
    if class_num:
        params["class-num"] = class_num

    course_results = []
    start = 1

    while True:
        # Send the GET request
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            data = response.json()

            # Assuming the response contains a dictionary with a 'courses' key
            courses = data[0]['COURSES']  # Use .get() for safe access
            retrievedrows = data[0]['RETRIEVEDROWS']
            lastcontrolnumber = data[0]['LASTCONTROLNUMBER']
            #totalrows = data[0]['TOTALROWS']

            if retrievedrows == 0 and lastcontrolnumber == 0:
                break

            # Iterate through each course in the courses list
            for i, course in enumerate(courses, start):
                course_code = course.get('code')
                sections = course.get('sections', [])

                # Print the course code and class numbers
                for section in sections:
                    class_number = section.get('classNumber')  # Extract class number
                    #print(f"{i}. {course_code} - {class_number}")
                    course_results.append({
                        "index": i,
                        "course_code": course_code,
                        "class_number": class_number
                    })

            #print(f"retrieved rows: {retrievedrows}")
            #print(f"lastcontrolnumber: {lastcontrolnumber}")
            #print(f"total rows: {totalrows}")
            #print(f"i: {i}")
            params['last-control-number'] = lastcontrolnumber
            start = i + 1

        else:
            print(f"Failed to retrieve data: {response.status_code}")

    return course_results


# Example usage
course = "COP"  # Example course code (can be None)
#class_num = 17940    # Example class number (can be None)
results = fetch_courses(course_code=course)

codes = [result['course_code'] for result in results]

if codes:
    print("\nRetrieved Courses:")
    for code in codes:
        print(code)

# Print out the results
#if results:
#    print("\nRetrieved Courses:")
#    for result in results:
#        print(f"Index: {result['index']}, Course Code: {result['course_code']}, Class Number: {result['class_number']}")
#else:
#    print("No courses retrieved.")
