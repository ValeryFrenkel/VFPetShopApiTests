import pytest
import allure
import requests
from tests.schemas.pet_schema import PET_SCHEMA
import jsonschema

BASE_URL = "http://5.181.109.28:9090/api/v3"


@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(
            self
    ):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(
            self
    ):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_nonexistent_pet(
            self
    ):
        with allure.step("Отправка запроса на получение несуществующего питомца"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_pet(
            self
    ):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }
        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json["id"] == payload["id"], "id питомца не совпадает с ожидаемым"
            assert response_json["name"] == payload["name"], "name питомца не совпадает с ожидаемым"
            assert response_json["status"] == payload["status"], "status питомца не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца c полными данными")
    def test_add_full_pet(
            self
    ):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {
                    "id": 1,
                    "name": "Dogs"
                },
                "photoUrls": ["string"],
                "tags": [{
                    "id": 0,
                    "name": "string"
                }],
                "status": "available"
            }
        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON схемы"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            jsonschema.validate(response_json, PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response_json["id"] == payload["id"], "id питомца не совпадает с ожидаемым"
            assert response_json["name"] == payload["name"], "name питомца не совпадает с ожидаемым"
            assert response_json["status"] == payload["status"], "status питомца не совпадает с ожидаемым"
            assert response_json["category"]["id"] == payload["category"]["id"], "id категории питомца не совпадает с ожидаемым"
            assert response_json["category"]["name"] == payload["category"]["name"], "name категории питомца не совпадает с ожидаемым"
            assert response_json["photoUrls"] == payload["photoUrls"], "photoUrls питомца не совпадает с ожидаемым"
            assert response_json["tags"] == payload["tags"], "tags питомца не совпадают с ожидаемым"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(
            self,
            create_pet
    ):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка зпроса на получение информации о питомце по ID"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.json()["id"] == pet_id, "ID питомца не совпал с ожидаемым"

    @allure.title("Обновление информации о питомце")
    def test_update_pet(
            self,
            create_pet
    ):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Подготовка данных для обновления питомца"):
            payload = {
                "id": pet_id,
                "name": "Buddy Updated",
                "status": "sold"
            }

        with allure.step("Отправка запроса на обновление питомца"):
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response_json["id"] == payload["id"], "ID питомца не совпал с ожидаемым"
            assert response_json["name"] == payload["name"], "name питомца не совпал с ожидаемым"
            assert response_json["status"] == payload["status"], "status питомца не совпал с ожидаемым"

    @allure.title("Удаление питомца по ID")
    def test_delete_pet_by_id(
            self,
            create_pet
    ):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на удаление питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса и текстового содержимого ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

        with allure.step("Проверка, что питомец действительно удалён"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Получение списка питомцев по статусу ")
    @pytest.mark.parametrize("status, expected_status_code", [
        ("available", 200),
        ("sold", 200),
        ("", 400),
        ("test",400)

    ])
    def test_get_pets_by_status(
            self,
            status,
            expected_status_code
    ):
        with allure.step("Отправка запроса на получение списка питомцев по статусу"):
            response = requests.get(
                url=f"{BASE_URL}/pet/findByStatus", params={
                    "status": f"{status}"
                }
            )

        with allure.step("Проверка статуса ответа и формата данных"):
            assert response.status_code == expected_status_code, "Код ответа не совпал с ожидаемым"
            if expected_status_code == 200:
                assert isinstance(response.json(), list)
            elif expected_status_code == 400:
                assert isinstance(response.json(), dict)
