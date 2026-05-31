import time
import allure
from jsonschema import validate
from schemas.booking_schema import BOOKING_SCHEMA


@allure.epic("E2E сценарий бронирования")
@allure.suite("E2E Booking Flow")
class TestBookingE2E:

    @allure.title("TC_E2E_001 Полный сценарий: Auth → Create → Get → Validate "
                  "→ Update → Check → Patch → Delete → Verify → Perf → Headers")
    def test_full_booking_flow(self, restful_client: "PlaywrightBookerAPI"):
        # === Шаг 1: Авторизация ===
        token = restful_client.authenticate("admin", "password123")
        assert token is not None

        # === Шаг 2: Создание брони ===
        booking_id, booking = restful_client.create_booking({
            "firstname": "John",
            "lastname": "Doe",
            "totalprice": 100,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2026-01-01",
                "checkout": "2026-01-05"
            }
        })
        assert booking_id is not None

        # === Шаг 3: Сохранение booking_id ===
        with allure.step("Сохранение идентификатора брони"):
            allure.attach(str(booking_id), "Booking ID", allure.attachment_type.TEXT)
            assert booking_id > 0

        # === Шаг 4: Получение брони по ID ===
        data = restful_client.get_booking(booking_id)
        assert data["firstname"] == "John"

        # === Шаг 5: Валидация схемы ===
        with allure.step("Валидация схемы ответа"):
            validate(instance=data, schema=BOOKING_SCHEMA)

        # === Шаг 6: Полное обновление (PUT) ===
        updated = restful_client.update_booking(booking_id, {
            "firstname": "Updated",
            "lastname": "Updated",
            "totalprice": 200,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2026-02-01",
                "checkout": "2026-02-10"
            },
            "additionalneeds": "Breakfast"
        })
        assert updated["firstname"] == "Updated"

        # === Шаг 7: Проверка обновления ===
        check_put = restful_client.get_booking(booking_id)
        assert check_put["lastname"] == "Updated"

        # === Шаг 8: Частичное обновление (PATCH) ===
        patched = restful_client.partial_update_booking(booking_id, {"totalprice": 200})
        assert patched["totalprice"] == 200

        # === Шаг 9: Удаление брони ===
        restful_client.delete_booking(booking_id)

        # === Шаг 10: Проверка удаления ===
        with allure.step("Проверка, что бронь удалена"):
            response_deleted = restful_client.context.get(f"{restful_client.base_url}/booking/{booking_id}")
            assert response_deleted.status == 404

        # === Шаг 11: Проверка производительности ===
        with allure.step("Проверка времени ответа (<2000 мс)"):
            start = time.perf_counter()
            response_perf = restful_client.context.get(f"{restful_client.base_url}/booking")
            duration = (time.perf_counter() - start) * 1000
            assert duration < 2000, f"Время ответа превышает 2000 мс: {duration:.2f} мс"

        # === Шаг 12: Проверка заголовков ===
        with allure.step("Проверка заголовка Content-Type"):
            content_type = response_perf.headers.get("Content-Type", "application/json")
            assert "application/json" in content_type