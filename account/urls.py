from django.urls import path
from django.contrib.auth.views import LoginView

from account import views
from account.forms import AccountAuthenticationForm

urlpatterns = [
    path('login', LoginView.as_view(
        template_name = 'account/login.html',
        authentication_form = AccountAuthenticationForm,
        extra_context = { 'title': 'Zaloguj' }
    ), name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout')
]