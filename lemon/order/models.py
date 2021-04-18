from django.db import models


class SIDES(models.TextChoices):
    BUY = "buy"
    SELL = "sell"


class Order(models.Model):
    """
    The heart of our little App is the Order model.
    It represents a trade made on our imaginary market and models either the buying
    or selling of a positive, non-zero quantity of some instrument. We support trading
    all types of instruments, as long as they are identified by a valid ISIN. We only
    execute orders that are valid as indicated by their deadline/time out. Orders can
    include an optional limit price.

    For more details on the ISIN specification, see:
    https://en.wikipedia.org/wiki/International_Securities_Identification_Number
    """

    isin = models.CharField(max_length=12)
    limit_price = models.DecimalField(null=True, max_digits=19, decimal_places=2)
    quantity = models.PositiveIntegerField()
    side = models.CharField(max_length=4, choices=SIDES.choices)
    valid_until = models.PositiveIntegerField()  # 32-bit int, matches UNIX timestamp
