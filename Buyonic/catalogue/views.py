from drf_yasg.openapi import Response

from .models import Product
from .serializers import ProductSerializer

from rest_framework.generics import GenericAPIView
from rest_framework import mixins,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from rest_framework import permissions

class IsManufacturer(permissions.BasePermission):
	message = 'Only Manufacturer can edit this page.'
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		else:
			try:
				return obj.is_manufacturer
			except:
				return obj.user == request.user


class ProductList(GenericAPIView):

    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated,]
    querset = Product.objects.all()

    def get(self,request):
        serializer = self.serializer_class()
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductDetails(GenericAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated,]
    def get(self,request,pk):
        product = Product.objects.get(id = pk)
        serializer = ProductSerializer(instance=product)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Order(GenericAPIView):
    pass