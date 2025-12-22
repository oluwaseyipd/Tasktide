from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task


class TaskAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="otheruser", password="otherpass123"
        )
        self.task = Task.objects.create(
            user=self.user,
            title="Test Task",
            description="Test Description",
            priority="medium",
        )
        self.task_url = reverse("task-detail", kwargs={"pk": self.task.pk})
        self.list_url = reverse("task-list")
        self.token_url = reverse("api-login")
        self.login()

    def login(self):
        response = self.client.post(
            "/api/users/login/",
            {"username": "testuser", "password": "testpass123"},
            format="json",
        )
        self.token = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_task_list_authenticated(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("results" in response.data)
        self.assertEqual(len(response.data["results"]), 1)

    def test_task_list_unauthenticated(self):
        self.client.credentials()  # Remove token
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task(self):
        data = {"title": "New Task", "description": "New Desc", "priority": "high"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.filter(user=self.user).count(), 2)

    def test_retrieve_task(self):
        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.task.title)

    def test_update_task(self):
        data = {"title": "Updated Task"}
        response = self.client.patch(self.task_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")

    def test_delete_task(self):
        response = self.client.delete(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())

    def test_cannot_access_others_task(self):
        # Login as another user
        response = self.client.post(
            "/api/users/login/",
            {"username": "otheruser", "password": "otherpass123"},
            format="json",
        )
        token2 = response.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token2}")
        response = self.client.get(self.task_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filtering_and_ordering(self):
        Task.objects.create(
            user=self.user,
            title="Another Task",
            description="Another Desc",
            priority="low",
            completed=True,
        )
        response = self.client.get(self.list_url + "?completed=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(task["completed"] for task in response.data["results"]))

    def test_pagination(self):
        # Create enough tasks to trigger pagination
        for i in range(15):
            Task.objects.create(user=self.user, title=f"Task {i}", priority="low")
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)

    def test_invalid_task_creation(self):
        # Missing required title
        data = {"description": "No title"}
        response = self.client.post(self.list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)
