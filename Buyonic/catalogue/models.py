from django.db import models
from accounts.models import MyUser

class Category(models.Model):
    category = models.CharField(max_length = 25)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category

class Product(models.Model):
    manufacturer = models.ForeignKey(MyUser, on_delete = models.CASCADE)
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    name = models.CharField(max_length = 25)
    cost = models.FloatField()
    description = models.TextField(max_length = 100)
    stock_status = models.BooleanField(default = True)
    created_on = models.DateTimeField(auto_now_add = True)
    photo = models.ImageField(blank = True)
    trend = models.IntegerField(default = 0)
    production_state = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-trend']


class Notify(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    below = models.FloatField()
    status = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.product} < {self.below}"

    class Meta:
        verbose_name_plural = "Notifications"

class Transaction(models.Model):
    final_payment = models.FloatField()

    def __str__(self):
        return self.id

class ManufacturerOrder(models.Model):
    user = models.ForeignKey(MyUser,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 0)
    total_cost = models.FloatField(default = 0)
    discount = models.FloatField(default = 0)
    confirmed = models.BooleanField(default = True)

    final_payment = models.FloatField(default = 0)

    def __str__(self):
        return f"Rs {self.discount} on {self.product.name}"

    def get_total_cost(self):
        total_cost = int(self.quantity) * int(self.product.cost)
        return int(total_cost)

class ClientOrder(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    m_order = models.ForeignKey(ManufacturerOrder, on_delete=models.CASCADE)
    quantity = models.IntegerField(default = 1)
    total_cost = models.FloatField(default = 0)
    shipping_charge = models.FloatField(default = 50)
    confirmed = models.BooleanField(default = False)
    refunded = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.product} : {self.quantity}"

    def get_total_cost(self):
        total_cost = int(self.quantity) * int(self.product.cost) + self.shipping_charge
        if total_cost >= int(self.user.refund_balance):
            total_cost -= int(self.user.refund_balance)
            self.user.refund_balance =0
        return int(total_cost)