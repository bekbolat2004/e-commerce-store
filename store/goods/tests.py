from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from goods.models import Categories, Products


class ProductTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Categories.objects.create(name="Phones", slug="phones")
        cls.product = Products.objects.create(
            name="Test phone",
            slug="test-phone",
            price=Decimal("99.99"),
            discount=Decimal("5.00"),
            quantity=3,
            category=category,
        )

    def test_sell_price_uses_decimal_percentage(self):
        self.assertEqual(self.product.sell_price(), Decimal("94.99"))

    def test_invalid_sort_field_is_ignored(self):
        response = self.client.get(
            reverse("category:catalog", args=["all"]),
            {"order_by": "unknown_field"},
        )

        self.assertEqual(response.status_code, 200)

    def test_invalid_page_falls_back_to_first_page(self):
        response = self.client.get(
            reverse("category:catalog", args=["all"]),
            {"page": "not-a-number"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["goods"].number, 1)

    def test_missing_product_returns_404(self):
        response = self.client.get(
            reverse("category:product", args=["does-not-exist"]),
        )

        self.assertEqual(response.status_code, 404)
