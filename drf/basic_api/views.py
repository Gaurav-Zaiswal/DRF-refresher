import logging
import json
from urllib import response

from django.http import Http404, JsonResponse
from django.forms import model_to_dict
from requests import delete

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Products
from .serializers import ProductSerializer


logging.basicConfig(
    level=logging.INFO,
    filename='logs/drf.log',
    format='%(asctime)s:%(name)s:%(message)s'
)

###################################################
#  APIs without use of DRF                        #
###################################################
def project_intro(request):
    # here the request is the instance of Django's HttpRequest class. 
    logging.info(f"headers:\n {request.headers}")
    logging.info(f"method:\n {request.method}")
    logging.info(f"content-type:\n {request.content_type}")
    logging.info(f"body:\n {request.body}") 
    # by default it is byte string (and not JSON) ref: https://docs.djangoproject.com/en/4.0/ref/request-response/#django.http.HttpRequest.body
    param={
        "messge":"hello world, this is Gaurav Jaiswal, and in this project I am refreshing my DRF concepts",
        "status": 200
    }
    # JsonRespons by default expects a dict and serializes to JSON
    return JsonResponse(param) 


def project_into_dynamic(request):
    body = request.body # byte string (of may be JSON, if sending JSON data)
    data ={}
    try:
        data = json.loads(body)
    except:
        pass
    name=data.get("name")
    param={
        "messge":"hello world, this is {name}, and in this project I am refreshing my DRF concepts",
        "status": 200
    }
    return JsonResponse(param)


def list_products_view(request):
    qs = Products.objects.all()
    # since that qs is the object of Quesryset
    # we have to change it from Quesryset -> Products -> dictionary -> json: process known as Serialization

    # to change object of quesyset to instance of Products model, use first() or filter()
    # ref: https://stackoverflow.com/a/45858176/10711551
    qs_model = qs.first()
    qs_model_dict = {}
    if qs:
        qs_model_dict = model_to_dict(qs_model)
    return JsonResponse(qs_model_dict)


###################################################
#          APIs with use of DRF                   #
###################################################
@api_view(http_method_names=["GET"])
def get_first_product(request):
    """
    using rest_framework's Response instead of JsonResponse
    """
    qs = Products.objects.all().first()
    if qs:
        qs_serializer = ProductSerializer(qs)
        data = qs_serializer.data
    return Response(data)

###################################################
#          one step further with DRF              #
###################################################
class ListProducts(APIView):
    """
    List all products, or create a new product.
    """
    def get(self, format=json):
        # get quesryset then serialize it then return serializer.data
        qs = Products.objects.all()
        serializer = ProductSerializer(qs, many=True) # it serializes whole queryset 
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        # get data from request
        # serialize the request.data then validate it by running is_valid() then save it
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DetailProduct(APIView):
    """
    Get a specific product or update, delete a Product instance
    """
    def get_product(self, pk):
        try:
            return Products.objects.get(pk=pk)
        except Products.DoesNotExist:
            return Http404 

    def get(self, request, pk):
        qs = self.get_product(pk=pk)
        serializer = ProductSerializer(qs)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        # get the instance first
        # then serialize it and validate it
        # if valid then 
        qs = self.get_product(pk=pk)
        # in case of PATCH (partial update)
        # qs is required and partial=True should be set
        serializer = ProductSerializer(qs, data=request.data, partial=True) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        # just get the instance and delete it, no need to serialize
        qs = self.get_product(pk=pk)
        qs.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

