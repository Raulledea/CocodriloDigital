from django.urls import path

from . import views

urlpatterns = [
    path('add_products/', views.add_product,name='add_products')
]
