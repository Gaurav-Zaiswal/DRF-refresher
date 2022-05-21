from django.urls import URLPattern
from django.urls import path

from .views import (
    project_intro, 
    project_into_dynamic,
    list_products_view,
    get_first_product,
    ListProducts,
    DetailProduct
)

urlpatterns=[
    path('', project_intro),
    path('dynamic/', project_into_dynamic),
    path('products-basic-listing/', list_products_view),
    path('products_drf_api/', get_first_product),
    path('products/', ListProducts.as_view()),
    path('product/<int:pk>/', DetailProduct.as_view()),
]