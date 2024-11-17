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

if __name__ == '__main__':
    app.run(debug=True)
