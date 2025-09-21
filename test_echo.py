import requests
import pytest

# Базовый URL сервиса PostmanEcho
BASE_URL = "https://postman-echo.com"

@pytest.fixture
def session():
    """
    Фикстура для создания сессии requests с общими заголовками.
    Упрощает тесты и избегает дублирования кода.
    """
    session = requests.Session()
    session.headers.update({
        "User-Agent": "PostmanEcho-Test-Automation",
        "Accept": "application/json"
    })
    return session


# === ТЕСТ 1: GET с query-параметрами ===
def test_get_with_query_params(session):
    """
    Проверяет, что GET-запрос с query-параметрами возвращает их в response.args.
    """
    params = {
        "key1": "value1",
        "user": "john_doe",
        "test": "123"
    }
    response = session.get(f"{BASE_URL}/get", params=params)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    json_data = response.json()
    assert json_data["args"] == params, f"Expected args {params}, got {json_data['args']}"
    assert json_data["url"] == f"{BASE_URL}/get?key1=value1&user=john_doe&test=123"


# === ТЕСТ 2: POST с JSON-телом ===
def test_post_with_json_body(session):
    """
    Проверяет, что POST с JSON-телом возвращает его в response.data и заголовок content-type.
    """
    json_body = {
        "name": "Alice",
        "age": 30,
        "city": "Moscow"
    }
    response = session.post(f"{BASE_URL}/post", json=json_body)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["data"] == json_body, f"Expected data {json_body}, got {json_data['data']}"
    assert json_data["headers"]["content-type"] == "application/json"


# === ТЕСТ 3: GET без query-параметров ===
def test_get_empty_args(session):
    """
    Проверяет, что GET без параметров возвращает пустой объект args.
    """
    response = session.get(f"{BASE_URL}/get")

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["args"] == {}, "Expected empty args object for empty query"


# === ТЕСТ 4: POST с form-data (x-www-form-urlencoded) ===
def test_post_with_form_data(session):
    """
    Проверяет, что POST с form-data возвращает данные в response.form и корректный content-type.
    """
    form_data = {
        "username": "testuser",
        "password": "secret123"
    }
    response = session.post(f"{BASE_URL}/post", data=form_data)

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["form"] == form_data, f"Expected form {form_data}, got {json_data['form']}"
    assert json_data["headers"]["content-type"] == "application/x-www-form-urlencoded"


# === ТЕСТ 5: Проверка кастомных заголовков ===
def test_custom_headers_in_response(session):
    """
    Проверяет, что кастомные заголовки, отправленные в запросе, отражаются в ответе.
    """
    custom_headers = {
        "X-Custom-Header": "test-value",
        "Accept-Language": "en-US"
    }
    # Обновляем заголовки сессии
    session.headers.update(custom_headers)

    response = session.get(f"{BASE_URL}/get")

    assert response.status_code == 200
    json_data = response.json()

    # Проверяем, что заголовки пришли в ответ (в нижнем регистре)
    assert json_data["headers"]["x-custom-header"] == "test-value"
    assert json_data["headers"]["accept-language"] == "en-US"

    # Проверяем, что оригинальные заголовки не возвращаются (все в lower-case)
    assert "X-Custom-Header" not in json_data["headers"]