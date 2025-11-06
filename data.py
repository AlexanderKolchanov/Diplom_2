# Данные тестового пользователя для проверки авторизации
class TestUser:
    email = 'alex_2025@ya.ru'
    password = 'secret123'
    name = 'Alexander'

# Данные пользователя для тестов изменения профиля
class UserForUpdate:
    email = 'alex_update@mail.ru'
    password = 'secret1234'
    name = 'Alexander'

# Данные ингредиентов для тестов заказов
class Ingredients:

    # Невалидные хеши ингредиентов для проверки ошибок
    invalid_hashes = ['61c0c5a71d1f82001bdaaa6', '16c0c5a71d1f82001bdaaa61']

# Ожидаемые ответы от API для различных сценариев
class ExpectedResponses:

     # Успешные операции
    success_true = {'success': True}
    # Пользователь уже существует
    user_already_exists = {'success': False, 'message': 'User already exists'}
    # Не заполнены обязательные поля
    missing_required_fields = {'success': False, 'message': 'Email, password and name are required fields'}
    # Неверные учетные данные
    invalid_credentials = {'success': False, 'message': 'email or password are incorrect'}
    # Неавторизованный доступ
    unauthorized_access = {'success': False, 'message': 'You should be authorised'}
    # Email уже используется
    email_already_taken = {'success': False, 'message': 'User with such email already exists'}
    # Не указаны ингредиенты
    no_ingredients_provided = {'success': False, 'message': 'Ingredient ids must be provided'}