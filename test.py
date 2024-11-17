import pytest
from crudActElect import app  

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_students(client):
    response = client.get('/api/students')
    assert response.status_code == 200
    data = response.get_json()
    assert 'success' in data and data['success'] is True
    assert 'students' in data

def test_get_single_student_found(client):
    response = client.get('/api/students/1')
    if response.status_code == 200:
        data = response.get_json()
        assert 'success' in data and data['success'] is True
        assert 'student' in data
    else:
        assert response.status_code == 404

def test_get_single_student_not_found(client):
    response = client.get('/api/students/999999')  
    assert response.status_code == 404
    data = response.get_json()
    assert 'success' in data and data['success'] is False
    assert data['error'] == 'Student not found'

def test_create_new_student(client):
    new_student = {
        "last_name": "Doe",
        "first_name": "Jane",
        "middle_name": "A.",
        "student_number": "789012",
        "gender": "Female",
        "birthdate": "1999-05-15"
    }
    response = client.post('/api/students', json=new_student)
    assert response.status_code == 201
    data = response.get_json()
    assert 'success' in data and data['success'] is True
    assert 'student' in data
    assert data['student']['last_name'] == "Doe"

def test_create_new_student_missing_field(client):
    incomplete_student = {
        "last_name": "Doe",
        "first_name": "Jane",
        "gender": "Female"
    }
    response = client.post('/api/students', json=incomplete_student)
    assert response.status_code == 400
    data = response.get_json()
    assert 'success' in data and data['success'] is False
    assert 'error' in data

def test_update_student(client):
    updated_student = {
        "first_name": "Johnathan"
    }
    response = client.put('/api/students/4', json=updated_student)
    if response.status_code == 200:
        data = response.get_json()
        assert 'success' in data and data['success'] is True
        assert data['message'] == 'Student updated successfully'
    else:
        assert response.status_code == 404

def test_delete_student(client):
    response = client.delete('/api/students/12')
    if response.status_code == 200:
        data = response.get_json()
        assert 'success' in data and data['success'] is True
        assert data['message'] == 'Student deleted successfully'
    else:
        assert response.status_code == 404

def test_404_error(client):
    response = client.get('/nonexistent-route')
    assert response.status_code == 404
    data = response.get_json()
    assert 'success' in data and data['success'] is False
    assert data['error'] == 'Resource not found'

def test_500_error(client, mocker):
    mocker.patch('conn.createConnection', return_value=None)
    response = client.get('/api/students')
    assert response.status_code == 500
    data = response.get_json()
    assert 'success' in data and data['success'] is False
    assert data['error'] == 'Database connection failed'
