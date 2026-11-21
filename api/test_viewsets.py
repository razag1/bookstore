from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Product, Order


class CategoryViewSetTests(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Livros")

    def test_list_categories(self):
        response = self.client.get(reverse("category-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_category(self):
        response = self.client.get(reverse("category-detail", args=[self.category.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Livros")

    def test_create_category(self):
        response = self.client.post(
            reverse("category-list"), {"name": "Tecnologia"}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_reject_category_without_name(self):
        response = self.client.post(reverse("category-list"), {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)


class ProductViewSetTests(APITestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Livros")
        self.product = Product.objects.create(
            name="Livro Python", price="90.00", category=self.category
        )

    def test_list_products(self):
        response = self.client.get(reverse("product-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["category"]["name"], "Livros")

    def test_retrieve_product(self):
        response = self.client.get(reverse("product-detail", args=[self.product.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Livro Python")

    def test_create_product(self):
        response = self.client.post(
            reverse("product-list"),
            {
                "name": "Livro Django",
                "price": "120.00",
                "category_id": self.category.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_reject_invalid_price(self):
        response = self.client.post(
            reverse("product-list"),
            {
                "name": "Livro Inválido",
                "price": "0.00",
                "category_id": self.category.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data)

    def test_reject_invalid_category(self):
        response = self.client.post(
            reverse("product-list"),
            {"name": "Livro Django", "price": "120.00", "category_id": 99999},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("category_id", response.data)

    def test_update_product(self):
        response = self.client.patch(
            reverse("product-detail", args=[self.product.id]),
            {"name": "Livro Python Avançado"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.product.refresh_from_db()

        self.assertEqual(self.product.name, "Livro Python Avançado")


class OrderViewSetTests(APITestCase):

    def setUp(self):
        category = Category.objects.create(name="Livros")

        self.product = Product.objects.create(
            name="Livro Python", price="90.00", category=category
        )

        self.order = Order.objects.create(product=self.product, quantity=2)

    def test_list_orders(self):
        response = self.client.get(reverse("order-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_order(self):
        response = self.client.post(
            reverse("order-list"),
            {"product": self.product.id, "quantity": 3},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)

    def test_reject_invalid_quantity(self):
        response = self.client.post(
            reverse("order-list"),
            {"product": self.product.id, "quantity": 0},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("quantity", response.data)

    def test_reject_invalid_product(self):
        response = self.client.post(
            reverse("order-list"), {"product": 99999, "quantity": 2}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("product", response.data)

    def test_delete_order(self):
        response = self.client.delete(reverse("order-detail", args=[self.order.id]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)
