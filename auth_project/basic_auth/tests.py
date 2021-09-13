from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from basic_auth.tools import is_user_valid


class UtilsTest(TestCase):
    def setUp(self):
        self.email = "example@example.com"
        self.password = "examplepassword"
        self.user = get_user_model().objects.get_or_create(email=self.email, is_verified=True)[0]
        self.user.set_password(self.password)
        self.user.save()

    def tearDown(self) -> None:
        self.user.delete()

    def test_is_user_valid(self):
        self.assertFalse(is_user_valid(self.email, "incorrect_password"))
        self.assertFalse(is_user_valid("incorrect_email@example.com", self.password))
        self.assertTrue(is_user_valid(self.email, self.password))


class LoginTest(APITestCase):
    def setUp(self) -> None:
        self.url = reverse("basic_auth:login")

        self.email = "example@example.com"
        self.password = "examplepassword"
        self.user = get_user_model().objects.get_or_create(email=self.email, is_verified=True)[0]
        self.user.set_password(self.password)
        self.user.save()

    def tearDown(self) -> None:
        self.user.delete()

    def test_successful_login(self):
        data = {
            "email": self.email,
            "password": self.password,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["authenticated"], True)

    def test_incorrect_password(self):
        data = {
            "email": self.email,
            "password": "incorrect_password",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_nonexistent_user(self):
        data = {
            "email": "invalidemail@invalid.com",
            "password": "invalidpassword",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_request_no_email(self):
        data = {
            "email": self.email,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_request_no_password(self):
        data = {
            "password": self.password,
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
