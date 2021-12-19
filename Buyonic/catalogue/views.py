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
        order_items = ClientOrder.objects.filter(product=product,confirmed=False)
        for item in order_items:
            product.trend += item.quantity
        serializer = ProductSerializer(instance=product)
        product.save()
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
        if product.production_state != user.state:
            order.shipping += (0.1)*order.get_total_cost()
        order.total_cost =  order.get_total_cost()
        order.save()
        return Response({'success':'success'})

class NotifyMe(GenericAPIView):

    serializer_class = NotifySerializer
    permission_classes = [IsAuthenticated,]

    def get(self,request,pk):
        user = request.user
        product = Product.objects.get(id=pk)
        notify = Notify.objects.filter(user=user,product=product)
        for note in notify:
            if note.product.cost <= note.below:
                note.status = True
                note.save()
        serializer = self.serializer_class(notify,many = True)
        return Response(serializer.data)

    def post(self,request,pk):
        user = request.user
        product = Product.objects.get(id=pk)
        below = request.data['below']
        notification = Notify(user=user,product=product,below = below)
        notification.save()
        return Response({'success':'success'})