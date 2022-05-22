import logging

from django.http import Http404, JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from basic_api.models import Products
from basic_api.serializers import ProductSerializer


logging.basicConfig(
    level=logging.INFO,
    filename='logs/drf.log',
    format='%(asctime)s:%(name)s:%(message)s'
)


'''
DRF comes with 4 default permission(Authorization) classes
1. AllowAny 
2. IsAuthenticated: only authenticated user can all the API
3. IsAuthenticatedOrReadOnly -> is the user is authorised then let them perform CRUD otherwise R only
4. IsAdminUser

ref: https://www.django-rest-framework.org/api-guide/permissions/

'''

class ListProducts(APIView):
    """
    List all products, or create a new product.
    """
    permission_classes = [IsAuthenticatedOrReadOnly] # only authenticated users can send POST request

    def get(self):
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
    permission_classes = [IsAuthenticatedOrReadOnly] # only authenticated users can send a PATCH/DELETE request

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

