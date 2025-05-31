import pytest
from flask import url_for

@pytest.fixture
def client():
    from app import create_app  
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_start_automation(client):
    response = client.post('/automation/start')
    assert response.status_code in (200, 400)  # Pode estar rodando ou ter iniciado
    data = response.get_json()
    assert 'message' in data

def test_stop_automation(client):
    response = client.post('/automation/stop')
    assert response.status_code in (200, 400)  # Pode ter parado ou não estava rodando
    data = response.get_json()
    assert 'message' in data

def test_status_automation(client):
    response = client.get('/automation/status')
    assert response.status_code == 200
    data = response.get_json()
    assert 'automation_active' in data
    assert isinstance(data['automation_active'], bool)

def test_get_products(client):
    response = client.get('/products')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)  # Lista de produtos

def test_get_product_not_found(client):
    response = client.get('/products/999999')  # ID que provavelmente não existe
    assert response.status_code == 404

@pytest.mark.skip(reason="Requer um produto com id=1 no banco de teste")
def test_get_product(client):
    response = client.get('/products/1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'id' in data and data['id'] == 1

@pytest.mark.skip(reason="Requer um produto com id=1 no banco de teste")
def test_get_product_history(client):
    response = client.get('/products/1/history')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
