#from drf_yasg.openapi import Response

import environ
from rest_framework.decorators import api_view,permission_classes
from . import Checksum
import requests
import json

from accounts.models import MyUser
from .models import Product,ClientOrder,Notify,Transaction
from .serializers import ProductSerializer,ClientOrderSerializer,NotifySerializer

from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import permissions
from django.shortcuts import render,redirect

env = environ.Env()
environ.Env.read_env()

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

    def get(self,request,pk):
        user = request.user
        order_list = ClientOrder.objects.filter(user=user,confirmed=False)
        serializer = self.serializer_class(order_list,many = True)
        return Response(serializer.data,status = status.HTTP_200_OK)
    
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
        return Response({'success':'success'},status = status.HTTP_201_CREATED)

    def put(self, request,pk):
        data = request.data
        user = request.user
        product = Product.objects.get(id=pk)
        order_item = ClientOrder.objects.get(user =user,product = product,confirmed = False)
        quantity = data.get('quantity')
        order_item.quantity = quantity
        order_item.save()
        return Response({'success': 'Item Updated successfully'}, status = status.HTTP_200_OK)	
		
    def delete(self, request,pk):
        user = request.user
        data = request.data
        product = Product.objects.get(id=pk)
        order_item = ClientOrder.objects.get(product=product)
        order_item.delete()
        return Response({'success': 'Item Removed successfully'}, status = status.HTTP_202_ACCEPTED)

class NotifyMe(GenericAPIView):

    serializer_class = NotifySerializer
    permission_classes = [IsAuthenticated,]

    def get(self,request,pk):
        user = request.user
        product = Product.objects.get(id=pk)
        notify = Notify.objects.filter(user=user)
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

class FinalOrder(GenericAPIView):
    serializer_class = ClientOrderSerializer
    permission_classes = [IsAuthenticated,]
    queryset = ClientOrder.objects.all()

    def get(self,request):
        user = request.user
        order_list = ClientOrder.objects.filter(user=user,confirmed=False)
        serializer = self.serializer_class(order_list,many = True)
        return Response(serializer.data)

    def post(self,request):
        user = request.user
        order_list = ClientOrder.objects.filter(user=user,confirmed=False)
        final_payment = 0
        for item in order_list:
            final_payment += item.total_cost
        transaction = Transaction.objects.create(final_payment=final_payment)
        param_dict = {
        'MID': env('MERCHANTID'),
        'ORDER_ID': str(transaction.id),
        'TXN_AMOUNT': str(final_payment),
        'CUST_ID': str(user.id),
        'INDUSTRY_TYPE_ID': 'Retail',
        'WEBSITE': 'WEBSTAGING',
        'CHANNEL_ID': 'WEB',
        'CALLBACK_URL': 'http://127.0.0.1:8000/product/handlepayment/',
    }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, env('MERCHANTKEY'))
        #return render(request,'checkout.html', context = param_dict)
        return Response()

@api_view(['POST'])
@permission_classes((IsAuthenticated, ))
def handlepayment(request):
    user = request.user
    checksum = ""
    form = request.POST

    response_dict = {}

    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

        if i == 'ORDERID':
            trans = Transaction.objects.get(id = id)

    verify = Checksum.verify_checksum(response_dict, env('MERCHANTKEY'), checksum)

    if verify:
        if response_dict['RESPCODE'] == '01':
            order_list = ClientOrder.objects.filter(user=user,confirmed=False)
            for item in order_list:
                item.confirmed = True
                item.save()
            print('order successful')
            return render(request, 'paymentstatus.html', {'response': response_dict})
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
            return render(request, 'paymentstatus.html', {'response': response_dict})