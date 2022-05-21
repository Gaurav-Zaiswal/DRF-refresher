from django.db import models

# Create your models here.

class Products(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.name}, {self.price}"
        