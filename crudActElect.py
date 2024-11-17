from flask import Flask, jsonify, request
from http import HTTPStatus
from mysql.connector import Error
from conn import createConnection  

app = Flask(__name__)

@app.route('/api/students', methods=['GET'])
def get_student_details(): 
    connection = createConnection() 
    if not connection:
        return jsonify({'success': False, 'error': 'Database connection failed'}), HTTPStatus.INTERNAL_SERVER_ERROR

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM student_details") 
        student_details = cursor.fetchall()  
        return jsonify({'success': True, 'students': student_details, 'total': len(student_details)}), HTTPStatus.OK
    except Error as e:
        return jsonify({'success': False, 'error': f"Database query failed: {e}"}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    connection = createConnection()
    if not connection:
        return jsonify({'success': False, 'error': 'Database connection failed'}), HTTPStatus.INTERNAL_SERVER_ERROR

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM student_details WHERE id = %s", (student_id,))
        student = cursor.fetchone()
        if student:
            return jsonify({'success': True, 'student': student}), HTTPStatus.OK
        return jsonify({'success': False, 'error': 'Student not found'}), HTTPStatus.NOT_FOUND
    except Error as e:
        return jsonify({'success': False, 'error': f"Database query failed: {e}"}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/api/students', methods=['POST'])
def create_new_student():
    if not request.json:
        return jsonify({'success': False, 'error': 'Request must be JSON'}), HTTPStatus.BAD_REQUEST

    student = request.json
    required_fields = ['last_name', 'first_name', 'middle_name', 'student_number', 'gender', 'birthdate']
    for field in required_fields:
        if field not in student:
            return jsonify({'success': False, 'error': f'{field} is required'}), HTTPStatus.BAD_REQUEST

    connection = createConnection()
    if not connection:
        return jsonify({'success': False, 'error': 'Database connection failed'}), HTTPStatus.INTERNAL_SERVER_ERROR

    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO student_details (last_name, first_name, middle_name, student_number, gender, birthdate) VALUES (%s, %s, %s, %s, %s, %s)",
            (student['last_name'], student['first_name'], student['middle_name'], student['student_number'], student['gender'], student['birthdate'])
        )
        connection.commit()
        new_id = cursor.lastrowid
        return jsonify({'success': True, 'student': {'id': new_id, **student}}), HTTPStatus.CREATED
    except Error as e:
        return jsonify({'success': False, 'error': f"Database query failed: {e}"}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            
@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    if not request.json:
        return jsonify({'success': False, 'error': 'Request must be JSON'}), HTTPStatus.BAD_REQUEST

    student = request.json
    fields_to_update = {key: value for key, value in student.items() if key in ['last_name', 'first_name', 'middle_name', 'student_number', 'gender', 'birthdate']}

    if not fields_to_update:
        return jsonify({'success': False, 'error': 'No valid fields to update'}), HTTPStatus.BAD_REQUEST

    connection = createConnection()
    if not connection:
        return jsonify({'success': False, 'error': 'Database connection failed'}), HTTPStatus.INTERNAL_SERVER_ERROR

    try:
        cursor = connection.cursor()
        updates = ", ".join(f"{field} = %s" for field in fields_to_update.keys())
        values = list(fields_to_update.values()) + [student_id]
        cursor.execute(f"UPDATE student_details SET {updates} WHERE id = %s", values)
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'success': False, 'error': 'Student not found'}), HTTPStatus.NOT_FOUND
        return jsonify({'success': True, 'message': 'Student updated successfully'}), HTTPStatus.OK
    except Error as e:
        return jsonify({'success': False, 'error': f"Database query failed: {e}"}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            
@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    connection = createConnection()
    if not connection:
        return jsonify({'success': False, 'error': 'Database connection failed'}), HTTPStatus.INTERNAL_SERVER_ERROR

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM student_details WHERE id = %s", (student_id,))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'success': False, 'error': 'Student not found'}), HTTPStatus.NOT_FOUND
        return jsonify({'success': True, 'message': 'Student deleted successfully'}), HTTPStatus.OK
    except Error as e:
        return jsonify({'success': False, 'error': f"Database query failed: {e}"}), HTTPStatus.INTERNAL_SERVER_ERROR
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            

if __name__ == '__main__':
    app.run(debug=True)
