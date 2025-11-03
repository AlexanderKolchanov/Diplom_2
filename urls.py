# Класс с эндпоинтами API Stellar Burgers
class Endpoints:
    # Базовый URL API
    base_url = 'https://stellarburgers.education-services.ru'
    # Регистрация нового пользователя
    register = '/api/auth/register'
    # Авторизация пользователя
    login = '/api/auth/login'
    # Выход из системы
    logout = '/api/auth/logout'
    # Обновление токена
    refresh_token = '/api/auth/token'
    # Удаление пользователя
    user_delete = '/api/auth/user'
    # Создание заказа
    create_order = '/api/orders'
    # Получение заказов пользователя
    user_orders = '/api/orders'
    # Получение ингредиентов
    ingredients = '/api/ingredients'  # Добавлен endpoint для ингредиентов