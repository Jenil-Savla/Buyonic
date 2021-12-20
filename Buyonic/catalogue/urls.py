from django.urls import path 
from . import views

urlpatterns = [
     path('',views.ProductList.as_view(),name="product-list"),
     path('details/<str:pk>',views.ProductDetails.as_view(),name="product-details"),
     path('order/',views.OrderForm.as_view(),name="MyOrders"),
     path('order/<str:pk>',views.OrderForm.as_view(),name="order-form"),
     path('notify/',views.NotifyMe.as_view(),name="notify-me"),
     path('notify/<str:pk>',views.NotifyMe.as_view(),name="notify-me"),
     path('pay/', views.FinalOrder.as_view(), name="payment"),
     path('handlepayment/', views.handlepayment, name="handlepayment"),
     path('manufacturer/', views.ManufacturerOrderList.as_view(), name="manufacturer-order"),
     path('manufacturer/<str:pk>', views.ManufacturerOrderView.as_view(), name="manufacturer-order"),
]