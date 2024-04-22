import sqlite3
import re

def validate_id(class_number, id_val):
    with sqlite3.connect('StudentCourse2.db') as conn:
        cursor = conn.cursor()
        query = '''
        SELECT first_name, last_name, class_number1, class_number2, class_number3, class_number4, 
               class_number5, class_number6, class_number7, class_number8 
        FROM student 
        WHERE UFID = ? OR ISO = ?
        '''
        cursor.execute(query, (id_val, id_val))
        result = cursor.fetchone()
        if result and class_number in result[2:]:
            return (True, result[0], result[1])
    return (False, '', '')

def validate_course(class_number):
    return bool(re.match(r'^\d{5}$', class_number))

def get_student_name(id_val):
    with sqlite3.connect('StudentCourse2.db') as conn:
        cursor = conn.cursor()
        query = '''
        SELECT first_name, last_name FROM student WHERE UFID = ? OR ISO = ?
        '''
        cursor.execute(query, (id_val, id_val))
        result = cursor.fetchone()
        return result[0] + ' ' + result[1] if result else ''
