from django.urls import path, include
from store_admin import views

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.users, name='users'),
    path('users/delete/<int:id>/', views.deleteuser, name='deleteuser'),
    path('users/edit/<int:id>', views.edituser, name='edituser'),
    path('categories/', views.categories, name='categories'),
    path('categories/add/', views.addcategory, name='addcategory'),
    path('categories/edit/<int:id>', views.editcategory, name='editcategory'),
    path('categories/delete/<int:id>', views.deletecategory, name='deletecategory'),
    path('products/', views.products, name='products'),
    path('products/add/', views.addproduct, name='addproduct'),
    path('products/delete/<int:id>/', views.deleteproduct, name='deleteproduct'),
    path('products/edit/<int:id>/', views.editproduct, name='editproduct'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:id>', views.orderdetails, name='orderdetails'),
]
