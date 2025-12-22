from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserAuthAPITests(APITestCase):
    def setUp(self):
        self.register_url = reverse("api-register")
        self.login_url = reverse("api-login")
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "testpass123",
        }
        self.user = User.objects.create_user(
            username="existinguser",
            email="existing@example.com",
            password="existingpass123",
        )

    def test_register_user_success(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertEqual(response.data["user"]["username"], self.user_data["username"])

    def test_register_user_duplicate_username(self):
        User.objects.create_user(
            username="testuser", email="other@example.com", password="otherpass"
        )
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_user_missing_fields(self):
        response = self.client.post(
            self.register_url, {"username": "noemail"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        response = self.client.post(
            self.login_url,
            {"username": "existinguser", "password": "existingpass123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_wrong_password(self):
        response = self.client.post(
            self.login_url,
            {"username": "existinguser", "password": "wrongpass"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_nonexistent_user(self):
        response = self.client.post(
            self.login_url, {"username": "nouser", "password": "nopass"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_permissions_protected_endpoint(self):
        # Example: try to access a protected endpoint (e.g., /api/tasks/) without authentication
        tasks_url = reverse("task-list")
        response = self.client.get(tasks_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
