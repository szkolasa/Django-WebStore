from django.urls import path

from profile import views

urlpatterns = [
    path('', views.home, name='home'),
    path('changepassword/', views.changePassword, name='changepassword'),
    path('changeemail/', views.changeemail, name='changeemail'),
    path('shipments/', views.shipments, name='shipments'),
    path('addshipment/', views.addshipment, name='addshipment'),
    path('deleteshipment/<int:id>/', views.deleteshipment, name='deleteshipment'),
    path('editshipment/<int:id>/', views.editshipment, name='editshipment'),
]