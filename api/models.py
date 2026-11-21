from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    description = models.TextField(blank=True)

    active = models.BooleanField(default=True)

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="orders"
    )

    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Pedido {self.pk}"
