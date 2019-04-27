from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def login(request):
    assert isinstance(request, HttpRequest)
    form = AuthenticationForm(request)
    return render(
        request,
        'account/login.html',
        {
            'title': 'Zaloguj',
            'form': form
        }
    )