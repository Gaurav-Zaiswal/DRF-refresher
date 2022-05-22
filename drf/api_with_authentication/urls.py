from django.urls import path

from .views import (
    ListProducts,
    DetailProduct
)

urlpatterns=[
    path('products/', ListProducts.as_view()),
    path('product/<int:pk>/', DetailProduct.as_view()),
]
