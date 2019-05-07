from django.urls import path, include
from store import views

urlpatterns = [
    path('', views.home, name='home'),
    path('getMenu/', views.menu, name='menu'),
    path('category/<int:id>', views.category, name='category'),
    path('products/list/<int:id>', views.productlist, name='productlist'),
    path('product/<int:id>', views.product, name='product'),
    path('cart/add/<int:id>', views.addtocart, name='addtocart'),
    path('cart/', views.cart, name='cart'),
    path('cart/items/', views.cartitems, name='cartitems'),
    path('cart/count/', views.itemsincart, name='cartcount'),
    path('product/name/<int:id>', views.productname, name='productname'),
    path('cart/remove/<int:id>', views.removeitem, name='removeitem'),
    path('cart/incqty/<int:id>', views.incqty, name='incqty'),
    path('cart/decqty/<int:id>', views.decqty, name='decqty'),
    path('cart/order/', views.order, name='order'),
    path('address/<int:id>/', views.getaddress, name='address'),
]