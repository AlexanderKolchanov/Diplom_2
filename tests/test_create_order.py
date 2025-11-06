import allure
import pytest
import requests
from urls import Endpoints
from data import Ingredients, ExpectedResponses
from generators import generate_ingredients_list


class TestOrderCreation:
    @allure.title('Создание заказа с авторизацией')
    def test_create_order_auth_success(self, authenticated_user, available_ingredients):
        """Создание заказа авторизованным пользователем"""
        # Формируем заголовок с токеном авторизации
        auth_header = {'Authorization': authenticated_user['accessToken']}
        # Генерируем список из 3 случайных ингредиентов для заказа
        payload = {'ingredients': generate_ingredients_list(3, available_ingredients)}
        
        with allure.step('Создание заказа с авторизацией'):
            response = requests.post(f'{Endpoints.base_url}{Endpoints.create_order}', data=payload, headers=auth_header)
        
        # Проверяем что заказ создан успешно
        assert response.status_code == 200
        assert response.json()['success'] == ExpectedResponses.success_true['success']


    @allure.title('Создание заказа с ингредиентами')
    def test_create_order_with_ingredients_success(self, authenticated_user, available_ingredients):
        """Создание заказа с указанием ингредиентов"""
        # Формируем заголовок с токеном авторизации
        auth_header = {'Authorization': authenticated_user['accessToken']}
        # Генерируем список из 2 случайных ингредиентов для заказа
        payload = {'ingredients': generate_ingredients_list(2, available_ingredients)}
        
        with allure.step('Создание заказа с ингредиентами'):
            response = requests.post(f'{Endpoints.base_url}{Endpoints.create_order}', data=payload, headers=auth_header)
        
        # Проверяем что заказ создан успешно
        assert response.status_code == 200
        assert response.json()['success'] == ExpectedResponses.success_true['success']


    @allure.title('Создание заказа без авторизации')
    def test_create_order_without_auth(self, available_ingredients):
        """Создание заказа без авторизации"""
        # Генерируем список из 1 случайного ингредиента
        payload = {'ingredients': generate_ingredients_list(1, available_ingredients)}
        
        with allure.step('Создание заказа без авторизации'):
            # Отправляем запрос без заголовка авторизации
            response = requests.post(f'{Endpoints.base_url}{Endpoints.create_order}', data=payload)
        
        # ИСПРАВЛЕНИЕ: API позволяет создавать заказы без авторизации
        assert response.status_code == 200
        assert response.json()['success'] == ExpectedResponses.success_true['success']


    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_no_ingredients(self, authenticated_user):
        """Создание заказа без указания ингредиентов"""
        # Формируем заголовок с токеном авторизации
        auth_header = {'Authorization': authenticated_user['accessToken']}
        # Создаем заказ с пустым списком ингредиентов
        payload = {'ingredients': []}
        
        with allure.step('Создание заказа без ингредиентов'):
            response = requests.post(f'{Endpoints.base_url}{Endpoints.create_order}', data=payload, headers=auth_header)
        
        # Проверяем что вернулась ошибка из-за отсутствия ингредиентов
        assert response.status_code == 400
        assert response.json() == ExpectedResponses.no_ingredients_provided
        

    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_invalid_ingredients(self, authenticated_user):
        """Создание заказа с невалидными ингредиентами"""
         # Формируем заголовок с токеном авторизации
        auth_header = {'Authorization': authenticated_user['accessToken']}
         # Используем заведомо невалидные хеши ингредиентов
        payload = {'ingredients': Ingredients.invalid_hashes}
    
        with allure.step('Создание заказа с невалидными ингредиентами'):
            response = requests.post(f'{Endpoints.base_url}{Endpoints.create_order}', data=payload, headers=auth_header)
    
        # "Если в запросе передан невалидный хеш ингредиента, вернется код ответа 500 Internal Server Error"
        assert response.status_code == 500