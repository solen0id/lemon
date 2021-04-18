from django.db import models


class SIDES(models.TextChoices):
    BUY = "buy"
    SELL = "sell"


class Order(models.Model):
    isin = models.CharField(max_length=12)
    limit_price = models.DecimalField(null=True, max_digits=19, decimal_places=2)
    quantity = models.PositiveIntegerField()
    side = models.CharField(max_length=4, choices=SIDES.choices)
    valid_until = models.PositiveIntegerField()  # 32-bit int, matches UNIX timestamp
