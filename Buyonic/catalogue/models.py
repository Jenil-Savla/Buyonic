from django.db import models
from accounts.models import MyUser

class Category(models.Model):
    category = models.CharField(max_length = 25)

class Product(models.Model):
    manufacturer = models.ForeignKey(MyUser, on_delete = models.CASCADE)
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    name = models.CharField(max_length = 25)
    cost = models.IntegerField()
    description = models.TextField(max_length = 100)
    stock_status = models.BooleanField(default = True)
    created_on = models.DateTimeField(auto_now_add = True)
    photo = models.ImageField(blank = True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['cost']