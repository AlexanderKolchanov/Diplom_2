import allure
import requests
import pytest
from urls import Endpoints
from data import TestUser, ExpectedResponses
from generators import generate_email, generate_password, generate_name


class TestUserRegistration:
    @allure.title('Создание пользователя')
    def test_create_user_success(self, new_user_data):
        """Создание пользователя с валидными данными"""
        # Берем сгенерированные данные пользователя из фикстуры
        payload = new_user_data
        
        with allure.step('Создание пользователя'):
            # Отправляем запрос на регистрацию
            response = requests.post(f'{Endpoints.base_url}{Endpoints.register}', data=payload)
        
        # Проверяем что пользователь создан успешно
        assert response.status_code == 200
        # Проверяем что в ответе вернулись корректные данные пользователя
        assert response.json()['user'] == {'email': payload['email'], 'name': payload['name']}
        # Проверяем флаг успеха операции
        assert response.json()['success'] == ExpectedResponses.success_true['success']


    @allure.title('Создание уже существующего пользователя')
    def test_create_existing_user(self, authenticated_user):
        """Создание пользователя с уже существующим email"""
        # Берем email из уже зарегистрированного пользователя
        existing_email = authenticated_user['user_data']['email']
        
        # Пытаемся зарегистрировать пользователя с тем же email
        payload = {
            'email': existing_email,
            'password': "any_password_123",
            'name': "Any Name"
        }
        
        with allure.step('Создание уже существующего пользователя'):
            response = requests.post(f'{Endpoints.base_url}{Endpoints.register}', data=payload)
        
        # Проверяем что вернулась ошибка "пользователь уже существует"
        assert response.status_code == 403
        assert response.json() == ExpectedResponses.user_already_exists
        

    @allure.title('Создание пользователя без указания одного из полей')
    @pytest.mark.parametrize('missing_field', ['email', 'password', 'name'])
    def test_create_user_missing_field(self, missing_field):
        """Создание пользователя без обязательного поля"""
        # Генерируем данные без одного поля в зависимости от параметра
        if missing_field == 'email':
            payload = {'password': generate_password(), 'name': generate_name()}
        elif missing_field == 'password':
            payload = {'email': generate_email(), 'name': generate_name()}
        else:  # missing_field == 'name'
            payload = {'email': generate_email(), 'password': generate_password()}
        
        with allure.step(f'Создание пользователя без поля {missing_field}'):
            response = requests.post(f'{Endpoints.base_url}{Endpoints.register}', data=payload)
        
        # Проверяем что вернулась ошибка из-за отсутствия обязательного поля
        assert response.status_code == 403
        assert response.json() == ExpectedResponses.missing_required_fields