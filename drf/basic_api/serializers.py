from dataclasses import field
from rest_framework.serializers import ModelSerializer

from .models import Products

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'description', 'price']

    