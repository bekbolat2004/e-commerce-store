from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class LoginRedirectTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alice",
            password="strong-test-password",
        )

    def test_login_allows_local_next_url(self):
        response = self.client.post(
            reverse("user:login"),
            {
                "username": "alice",
                "password": "strong-test-password",
                "next": reverse("user:profile"),
            },
        )

        self.assertRedirects(response, reverse("user:profile"))

    def test_login_rejects_external_next_url(self):
        response = self.client.post(
            reverse("user:login"),
            {
                "username": "alice",
                "password": "strong-test-password",
                "next": "https://evil.example/phishing",
            },
        )

        self.assertRedirects(response, reverse("main:index"))

    def test_basket_page_requires_login(self):
        response = self.client.get(reverse("user:users_basket"))

        self.assertRedirects(
            response,
            f"{reverse('user:login')}?next={reverse('user:users_basket')}",
        )
