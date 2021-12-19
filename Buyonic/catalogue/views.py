from drf_yasg.openapi import Response
from rest_framework.serializers import Serializer

from accounts.models import MyUser
from .models import Product,ClientOrder,Notify
from .serializers import ProductSerializer,ClientOrderSerializer,NotifySerializer

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

    def get(self,request):
        product = Product.objects.all()
        serializer = self.serializer_class(product,many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductDetails(GenericAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated,]
    def get(self,request,pk):
        product = Product.objects.get(id = pk)
        serializer = ProductSerializer(instance=product)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderForm(GenericAPIView):

    serializer_class = ClientOrderSerializer
    permission_classes = [IsAuthenticated,]

    def post(self,request,pk):
        data = request.data
        user = request.user
        product = Product.objects.get(id=pk)
        quantity = data['quantity']
        order = ClientOrder(user=user,product=product, quantity=quantity)
        order.total_cost =  order.get_total_cost()
        order.save()
        return Response({'success':'success'})