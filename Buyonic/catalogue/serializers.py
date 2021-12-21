from rest_framework import serializers

from .models import ManufacturerOrder, Product,Category,ClientOrder,Notify
from accounts.models import MyUser
from accounts.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    manufacturer = UserSerializer()
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = '__all__'

    def create(self,validated_data):
        category_data = validated_data.pop('category')
        category = Category.objects.get(category = category_data['category'])
        product = Product.objects.create(category=category,**validated_data)
        return product

class ClientOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = ClientOrder
        fields = ['product','quantity','total_cost']

class NotifySerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Notify
        fields = '__all__'

class ManufacturerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManufacturerOrder
        fields = '__all__'