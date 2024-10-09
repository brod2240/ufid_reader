import unittest
import requests

class TestExternalAPI(unittest.TestCase):

    # Roster GET no parameters
    def test_roster_get_1(self):
        url = "https://gatorufid.pythonanywhere.com/roster"

        response = requests.get(url)        

        # Check the status code
        self.assertEqual(response.status_code, 200)

        # returns the template
        # print(response.text)
    
    # Roster GET only serial
    def test_roster_get_2(self):
        url = "https://gatorufid.pythonanywhere.com/roster"

        params = {'serial_num': '10000000d340eb60'}

        response = requests.get(url, params=params)        

        # Check the status code
        self.assertEqual(response.status_code, 400)

        # Check the response content
        data = response.json()

        self.assertEqual(data['error'], 'Serial number exists but no additional parameters provided')

    # Roster GET only ISO
    def test_roster_get_3(self):
        url = "https://gatorufid.pythonanywhere.com/roster"

        params = {'iso': '1234567812345678'}

        response = requests.get(url, params=params)        

        # Check the status code
        self.assertEqual(response.status_code, 200)

        # returns the template
        # print(response.text)

    # Roster GET only UFID
    def test_roster_get_4(self):
        url = "https://gatorufid.pythonanywhere.com/roster"

        params = {'iso': '1234567812345678'}

        response = requests.get(url, params=params)        

        # Check the status code
        self.assertEqual(response.status_code, 200)

        # returns the template
        # print(response.text)

    # Roster GET invalid serial
    def test_roster_get_5(self):
        url = "https://gatorufid.pythonanywhere.com/roster"

        params = {'serial_num': '20000000d340eb60', 'iso': '1234567812345678'}

        response = requests.get(url, params=params)        

        # Check the status code
        self.assertEqual(response.status_code, 404)

        # Check the response content
        data = response.json()

        self.assertEqual(data['error'], 'Serial number not found')

    # Roster GET invalid ISO
    def test_roster_get_6(self):
        url = "https://gatorufid.pythonanywhere.com/roster"

        params = {'serial_num': '10000000d340eb60', 'iso': '3000000000000000'}

        response = requests.get(url, params=params)        

        # Check the status code
        self.assertEqual(response.status_code, 404)

        # Check the response content
        data = response.json()

        self.assertEqual(data['error'], 'UFID or ISO not found')

    # Roster GET invalid UFID
    def test_roster_get_7(self):
        url = "https://gatorufid.pythonanywhere.com/roster"

        params = {'serial_num': '10000000d340eb60', 'ufid': '30000000'}

        response = requests.get(url, params=params)        

        # Check the status code
        self.assertEqual(response.status_code, 404)

        # Check the response content
        data = response.json()

        self.assertEqual(data['error'], 'UFID or ISO not found')

    # Roster GET valid ISO
    def test_roster_get_8(self):
        url = "https://gatorufid.pythonanywhere.com/roster"

        params = {'serial_num': '10000000d340eb60', 'iso': '2000000000000000'}

        response = requests.get(url, params=params)        

        # Check the status code
        self.assertEqual(response.status_code, 200)

        # Check the response content
        data = response.json()

        self.assertEqual(data['student_data'], ['20000000', '2000000000000000', 'Jimmy', 'Johns', '29563', '12345', None, None, None, None, None, None])

     # Roster GET valid UFID
    def test_roster_get_9(self):
        url = "https://gatorufid.pythonanywhere.com/roster"

        params = {'serial_num': '10000000d340eb60', 'ufid': '20000000'}

        response = requests.get(url, params=params)        

        # Check the status code
        self.assertEqual(response.status_code, 200)

        # Check the response content
        data = response.json()

        self.assertEqual(data['student_data'], ['20000000', '2000000000000000', 'Jimmy', 'Johns', '29563', '12345', None, None, None, None, None, None])

    # PiConfig/Kiosks GET no parameters
    def test_kiosks_get_1(self):
        url = "https://gatorufid.pythonanywhere.com/kiosks"

        response = requests.get(url)        

        # Check the status code
        self.assertEqual(response.status_code, 200)

        # Returns Template
        # print(response.text)

    # PiConfig/Kiosks GET invalid serial
    def test_kiosks_get_2(self):
        url = "https://gatorufid.pythonanywhere.com/kiosks"

        params = {'serial_num': '20000000d340eb60'}

        response = requests.get(url, params=params)        

        # Check the status code
        self.assertEqual(response.status_code, 404)

        # Check the response content
        data = response.json()

        self.assertEqual(data['error'], 'Serial number not found')

    # PiConfig/Kiosks GET valid serial
    def test_kiosks_get_3(self):
        url = "https://gatorufid.pythonanywhere.com/kiosks"

        params = {'serial_num': '10000000d340eb60'}

        response = requests.get(url, params=params)        

        # Check the status code
        self.assertEqual(response.status_code, 200)

        # Check the response content
        data = response.json()

        self.assertEqual(data['room_num'], 'NSC215')

    # Courses GET no parameter
    def test_courses_get_1(self):
        url = "https://gatorufid.pythonanywhere.com/courses"

        response = requests.get(url)        

        # Check the status code
        self.assertEqual(response.status_code, 400)

        # Check the response content
        data = response.json()

        # Since no day is provided
        self.assertEqual(data['error'], 'Invalid or no day provided')

    # Courses GET only day
    def test_courses_get_2(self):
        url = "https://gatorufid.pythonanywhere.com/courses"

        params = {'day': 'T'}

        response = requests.get(url, params=params)        

        # Check the status code
        self.assertEqual(response.status_code, 200)

        # Check the response content
        data = response.json()

        # Returns empty list since no roomCode provided
        self.assertEqual(data, [])

    # Courses GET only roomCode
    def test_courses_get_3(self):
        url = "https://gatorufid.pythonanywhere.com/courses"

        params = {'roomCode': 'NSC215'}

        response = requests.get(url, params=params)        

        # Check the status code
        self.assertEqual(response.status_code, 400)

        # Check the response content
        data = response.json()

        # Since no day is provided
        self.assertEqual(data['error'], 'Invalid or no day provided')

    # Courses GET invalid day
    def test_courses_get_4(self):
        url = "https://gatorufid.pythonanywhere.com/courses"

        params = {'day': 'Sun', 'roomCode': 'NSC215'}

        response = requests.get(url, params=params)        

        # Check the status code
        self.assertEqual(response.status_code, 400)

        # Check the response content
        data = response.json()

        # Since no day is provided
        self.assertEqual(data['error'], 'Invalid or no day provided')

    # Courses GET invalid room
    def test_courses_get_5(self):
        url = "https://gatorufid.pythonanywhere.com/courses"

        params = {'day': 'T', 'roomCode': 'NSC2152'}

        response = requests.get(url, params=params)        

        # Check the status code
        self.assertEqual(response.status_code, 200)

        # Check the response content
        data = response.json()

        # Returns empty list since invalid roomCode provided
        self.assertEqual(data, [])

    # Courses GET valid day and room
    def test_courses_get_6(self):
        url = "https://gatorufid.pythonanywhere.com/courses"

        params = {'day': 'T', 'roomCode': 'NSC215'}

        response = requests.get(url, params=params)        

        # Check the response content
        data = response.json()

        self.assertEqual(data, [['CEN3907C', '24160', 'Carsten Thue-Bludworth', '3', "['T', 'R']", '10:40 AM', '12:35 PM', 'NSC215'], ['CEN4908C', '29563', 'Carsten Thue-Bludworth', '1', "['T', 'R']", '10:40 AM', '12:35 PM', 'NSC215']])

if __name__ == '__main__':
    unittest.main()