from flaskr import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'

def test_info(client):
    data = client.get('/linreg/info').json()
    assert float(data["coefficients"]) > 0