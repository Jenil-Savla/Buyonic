from drf_yasg.openapi import Response
from rest_framework import serializers
from rest_framework.serializers import Serializer
from .models import Product
from .serializers import ProductSerializer

from rest_framework.generics import GenericAPIView
from rest_framework import mixins,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class ProductList(mixins.ListModelMixin,GenericAPIView):

    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated,]
    querset = Product.objects.all()

    def get(self,request):
        serializer = self.serializer_class()
        return Response(serializer.data, status=status.HTTP_200_OK)