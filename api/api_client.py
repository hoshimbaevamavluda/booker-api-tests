import allure
from playwright.sync_api import APIRequestContext
from typing import Optional, Dict, Any


class PlaywrightBookerAPI:
    """API Client через Playwright request context"""

    def __init__(self, context: APIRequestContext, base_url: str, auth_token: Optional[str] = None):
        self.context = context
        self.base_url = base_url
        self.auth_token = auth_token

    def _get_headers(self, require_auth: bool = True) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if require_auth and self.auth_token:
            headers["Cookie"] = f"token={self.auth_token}"
        return headers

    def authenticate(self, username: str, password: str) -> str:
        with allure.step(f"Аутентификация пользователя {username}"):
            response = self.context.post(
                f"{self.base_url}/auth",
                data={"username": username, "password": password}
            )
            assert response.ok, f"Auth failed: {response.status}"
            data = response.json()
            allure.attach(str(data), "Auth Response", allure.attachment_type.JSON)
            self.auth_token = data["token"]
            return self.auth_token

    def create_booking(self, booking_data: Dict[str, Any]) -> tuple[int, Dict[str, Any]]:
        with allure.step("Создание бронирования"):
            response = self.context.post(
                f"{self.base_url}/booking",
                data=booking_data,
                headers=self._get_headers(require_auth=True)
            )
            assert response.ok, f"Create booking failed: {response.status}"
            data = response.json()
            allure.attach(str(data), "Booking Response", allure.attachment_type.JSON)
            return data["bookingid"], data["booking"]

    def get_booking(self, booking_id: int) -> Dict[str, Any]:
        with allure.step(f"Получение брони по ID {booking_id}"):
            response = self.context.get(
                f"{self.base_url}/booking/{booking_id}",
                headers=self._get_headers(require_auth=True)
            )
            assert response.ok, f"Get booking failed: {response.status}"
            data = response.json()
            allure.attach(str(data), f"Booking {booking_id}", allure.attachment_type.JSON)
            return data

    def update_booking(self, booking_id: int, booking_data: Dict[str, Any]) -> Dict[str, Any]:
        with allure.step(f"Полное обновление брони {booking_id}"):
            response = self.context.put(
                f"{self.base_url}/booking/{booking_id}",
                data=booking_data,
                headers=self._get_headers(require_auth=True)
            )
            assert response.ok, f"Update booking failed: {response.status}"
            data = response.json()
            allure.attach(str(data), f"Updated Booking {booking_id}", allure.attachment_type.JSON)
            return data

    def partial_update_booking(self, booking_id: int, booking_data: Dict[str, Any]) -> Dict[str, Any]:
        with allure.step(f"Частичное обновление брони {booking_id}"):
            response = self.context.patch(
                f"{self.base_url}/booking/{booking_id}",
                data=booking_data,
                headers=self._get_headers(require_auth=True)
            )
            assert response.ok, f"Partial update failed: {response.status}"
            data = response.json()
            allure.attach(str(data), f"Patched Booking {booking_id}", allure.attachment_type.JSON)
            return data

    def delete_booking(self, booking_id: int) -> None:
        with allure.step(f"Удаление брони {booking_id}"):
            response = self.context.delete(
                f"{self.base_url}/booking/{booking_id}",
                headers=self._get_headers(require_auth=True)
            )
            assert response.ok, f"Delete booking failed: {response.status}"
            allure.attach(f"Booking {booking_id} deleted", "Delete Result", allure.attachment_type.TEXT)
