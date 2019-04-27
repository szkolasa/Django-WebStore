from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.

def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'store/home.html',
        {
            'title': 'Home'
        }
    )