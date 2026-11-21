from django.test import TestCase

from .models import Category, Product, Order
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    OrderSerializer,
)


class CategorySerializerTest(TestCase):

    def test_accepts_valid_data(self):
        data = {"name": "Livros"}

        serializer = CategorySerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_requires_name(self):
        serializer = CategorySerializer(data={})

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_creates_category(self):
        serializer = CategorySerializer(data={"name": "Tecnologia"})

        self.assertTrue(serializer.is_valid(), serializer.errors)

        category = serializer.save()

        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(category.name, "Tecnologia")

    def test_returns_expected_fields(self):
        category = Category.objects.create(name="Livros")

        serializer = CategorySerializer(category)

        self.assertEqual(set(serializer.data.keys()), {"id", "name"})


class ProductSerializerTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Periféricos")

        self.valid_data = {
            "name": "Teclado",
            "price": "150.00",
            "description": "Teclado mecânico",
            "active": True,
            "category_id": self.category.id,
        }

    def test_accepts_valid_data(self):
        serializer = ProductSerializer(data=self.valid_data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_requires_name(self):
        data = self.valid_data.copy()
        data.pop("name")

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_requires_price(self):
        data = self.valid_data.copy()
        data.pop("price")

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("price", serializer.errors)

    def test_requires_category(self):
        data = self.valid_data.copy()
        data.pop("category_id")

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("category_id", serializer.errors)

    def test_rejects_zero_price(self):
        data = self.valid_data.copy()
        data["price"] = "0.00"

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("price", serializer.errors)

    def test_rejects_invalid_category(self):
        data = self.valid_data.copy()
        data["category_id"] = 99999

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("category_id", serializer.errors)

    def test_creates_product(self):
        serializer = ProductSerializer(data=self.valid_data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

        product = serializer.save()

        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(product.name, "Teclado")
        self.assertEqual(str(product.price), "150.00")
        self.assertEqual(product.category, self.category)

    def test_returns_nested_category(self):
        product = Product.objects.create(
            name="Mouse", price="80.00", category=self.category
        )

        serializer = ProductSerializer(product)

        self.assertEqual(serializer.data["category"]["name"], "Periféricos")

        self.assertEqual(
            set(serializer.data.keys()),
            {
                "id",
                "name",
                "price",
                "description",
                "active",
                "category",
            },
        )


class OrderSerializerTest(TestCase):

    def setUp(self):
        category = Category.objects.create(name="Livros")

        self.product = Product.objects.create(
            name="Livro Python", price="90.00", category=category
        )

    def test_accepts_valid_data(self):
        serializer = OrderSerializer(
            data={
                "product": self.product.id,
                "quantity": 2,
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_requires_product(self):
        serializer = OrderSerializer(
            data={
                "quantity": 2,
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("product", serializer.errors)

    def test_requires_quantity(self):
        serializer = OrderSerializer(
            data={
                "product": self.product.id,
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("quantity", serializer.errors)

    def test_rejects_zero_quantity(self):
        serializer = OrderSerializer(
            data={
                "product": self.product.id,
                "quantity": 0,
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("quantity", serializer.errors)

    def test_rejects_invalid_product(self):
        serializer = OrderSerializer(
            data={
                "product": 99999,
                "quantity": 2,
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("product", serializer.errors)

    def test_creates_order(self):
        serializer = OrderSerializer(
            data={
                "product": self.product.id,
                "quantity": 3,
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        order = serializer.save()

        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.quantity, 3)

    def test_returns_expected_fields(self):
        order = Order.objects.create(product=self.product, quantity=2)

        serializer = OrderSerializer(order)

        self.assertEqual(set(serializer.data.keys()), {"id", "product", "quantity"})
