from django.db import models


class Restaurant(models.Model):
    name = models.CharField(
        max_length=100,
    )

    address = models.CharField(
        max_length=150,
    )

    phone = models.CharField(
        max_length=30,
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
    )

    def __str__(self):
        return self.name


class Dish(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=100,
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,

    )

    status = models.CharField(
        max_length=50,

    )

    def __str__(self):
        return self.name


class Client(models.Model):
    full_name = models.CharField(
        max_length=100,
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=30,
    )

    delivery_address = models.CharField(
        max_length=150,
    )

    def __str__(self):
        return self.full_name



class Courier(models.Model):
    full_name = models.CharField(
        max_length=100,

    )

    phone = models.CharField(
        max_length=30,

    )

    transport = models.CharField(
        max_length=50,

    )

    status = models.CharField(
        max_length=50,

    )

    def __str__(self):
        return self.full_name



class Order(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,

    )

    courier = models.ForeignKey(
        Courier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,

    )

    order_date = models.DateTimeField(
        auto_now_add=True,

    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,

    )

    status = models.CharField(
        max_length=50,

    )

    def __str__(self):
        return f'Заказ №{self.id}'



class OrderItem(models.Model):
    dish = models.ForeignKey(
        Dish,
        on_delete=models.CASCADE,

    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,

    )

    quantity = models.PositiveIntegerField(
    )

    def __str__(self):
        return f'{self.dish.name} — {self.quantity} шт.'
