from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    shop_src_id = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_link = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    description = models.TextField()
    product_link = models.CharField(max_length=255)
    product_src_id = models.CharField(db_index=True, max_length=255)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name





