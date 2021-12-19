from rest_framework import serializers

from .models import Product,Category,ClientOrder,Notify
from accounts.models import MyUser

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer
    class Meta:
        model = Product
        fields = '__all__'

    def create(self,validated_data):
        category_data = validated_data.pop('category')
        category = Category.objects.get(category = category_data['category'])
        product = Product.objects.create(category=category,**validated_data)
        return product

class ClientOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientOrder
        fields = ['quantity',]

class NotifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Notify
        fields = '__all__'