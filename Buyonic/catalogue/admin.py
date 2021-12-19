from django.contrib import admin
from .models import Product,Category,ClientOrder,Notify

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ClientOrder)
admin.site.register(Notify)