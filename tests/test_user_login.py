import allure
import requests
import pytest
from urls import Endpoints
from data import TestUser, ExpectedResponses
from generators import generate_email, generate_password


class TestUserLogin:
    @allure.title('Вход под существующим пользователем')
    def test_login_success(self, authenticated_user):
        """Вход с валидными учетными данными"""
        # Берем данные уже зарегистрированного пользователя из фикстуры
        user_data = authenticated_user['user_data']
        payload = {
            'email': user_data['email'],
            'password': user_data['password']
        }
        
        with allure.step('Вход с корректными данными'):
            response = requests.post(Endpoints.login, data=payload)
        
        # Проверяем что авторизация прошла успешно
        assert response.status_code == 200
        # Проверяем что в ответе вернулись корректные данные пользователя
        assert response.json()['user']['email'] == user_data['email']
        # Проверяем флаг успеха операции
        assert response.json()['success'] == ExpectedResponses.success_true['success']
        

    @allure.title('Вход с неверными учетными данными')
    @pytest.mark.parametrize('wrong_email, wrong_password', [
        [True, False],  # Неверный email, правильный пароль
        [False, True]   # Правильный email, неверный пароль
    ])
    def test_login_invalid_credentials(self, authenticated_user, wrong_email, wrong_password):
        """Вход с неверными учетными данными"""
        # Берем данные зарегистрированного пользователя
        user_data = authenticated_user['user_data']
        
        # Формируем данные для входа: либо неверный email, либо неверный пароль
        payload = {
            'email': generate_email() if wrong_email else user_data['email'],
            'password': generate_password() if wrong_password else user_data['password']
        }
        
        with allure.step('Вход с неверными данными'):
            response = requests.post(Endpoints.login, data=payload)
        
        # Проверяем что вернулась ошибка авторизации
        assert response.status_code == 401
        assert response.json() == ExpectedResponses.invalid_credentials