import pytest
import requests
from generators import generate_email, generate_password, generate_name
from urls import Endpoints


@pytest.fixture()
def new_user_data():
    """Данные нового пользователя с автоматическим удалением после теста"""
    payload = {
        'email': generate_email(),
        'password': generate_password(),
        'name': generate_name()
    }
    yield payload
    payload_login = {
        'email': payload['email'],
        'password': payload['password']
    }
    response = requests.post(Endpoints.login, data=payload_login)
    requests.delete(Endpoints.user_delete, headers={'Authorization': response.json()['accessToken']})


@pytest.fixture()
def authenticated_user():
    """Авторизованный пользователь"""
    # Делаем несколько попыток с разными данными
    for _ in range(3):
        user_data = {'email': generate_email(), 'password': generate_password(), 'name': generate_name()}
        
        # Регистрируем пользователя
        register_response = requests.post(Endpoints.register, data=user_data)
        
        # Авторизуемся
        login_response = requests.post(Endpoints.login, 
                                      data={'email': user_data['email'], 'password': user_data['password']})
        
        # Если авторизация успешна - возвращаем данные
        if login_response.status_code == 200:
            response_data = login_response.json()
            response_data['user_data'] = user_data
            return response_data
    
    # Если все попытки неудачны
    pytest.fail("Failed to create and authenticate user after 3 attempts")


@pytest.fixture(scope='session')
def available_ingredients():
    """Список ID ингредиентов"""
    response = requests.get(Endpoints.ingredients)
    assert response.status_code == 200, "Failed to get ingredients"
    return [ingredient['_id'] for ingredient in response.json()['data']]