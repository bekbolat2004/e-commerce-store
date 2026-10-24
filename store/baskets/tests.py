from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from baskets.models import Basket
from goods.models import Categories, Products


class BasketViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user("owner", password="test-password")
        cls.other_user = get_user_model().objects.create_user("other", password="test-password")
        category = Categories.objects.create(name="Phones", slug="phones")
        cls.product = Products.objects.create(
            name="Phone",
            slug="phone",
            price="100.00",
            quantity=2,
            category=category,
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_add_requires_post(self):
        response = self.client.get(reverse("basket:basket_add", args=[self.product.slug]))

        self.assertEqual(response.status_code, 405)
        self.assertFalse(Basket.objects.exists())

    def test_add_creates_and_increments_one_basket(self):
        url = reverse("basket:basket_add", args=[self.product.slug])

        self.client.post(url)
        self.client.post(url)

        basket = Basket.objects.get(user=self.user, product=self.product)
        self.assertEqual(basket.quantity, 2)
        self.assertEqual(Basket.objects.count(), 1)

    def test_add_does_not_exceed_stock(self):
        Basket.objects.create(user=self.user, product=self.product, quantity=2)

        self.client.post(reverse("basket:basket_add", args=[self.product.slug]))

        self.assertEqual(Basket.objects.get(user=self.user).quantity, 2)

    def test_out_of_stock_product_is_not_added(self):
        self.product.quantity = 0
        self.product.save(update_fields=["quantity"])

        self.client.post(reverse("basket:basket_add", args=[self.product.slug]))

        self.assertFalse(Basket.objects.exists())

    def test_user_cannot_remove_another_users_basket(self):
        basket = Basket.objects.create(user=self.other_user, product=self.product, quantity=1)

        response = self.client.post(reverse("basket:basket_remove", args=[basket.id]))

        self.assertEqual(response.status_code, 404)
        self.assertTrue(Basket.objects.filter(id=basket.id).exists())

    def test_owner_can_change_quantity(self):
        basket = Basket.objects.create(user=self.user, product=self.product, quantity=1)

        self.client.post(
            reverse("basket:basket_change", args=[basket.id]),
            {"quantity": 2},
        )

        basket.refresh_from_db()
        self.assertEqual(basket.quantity, 2)

    def test_invalid_quantity_is_rejected(self):
        basket = Basket.objects.create(user=self.user, product=self.product, quantity=1)

        self.client.post(
            reverse("basket:basket_change", args=[basket.id]),
            {"quantity": 99},
        )

        basket.refresh_from_db()
        self.assertEqual(basket.quantity, 1)
