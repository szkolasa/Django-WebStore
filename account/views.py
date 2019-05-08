from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from account.forms import AccountUserCreationForm

# Create your views here.

def register(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = AccountUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = auth.authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            auth.login(request, new_user)
            return redirect('store:home')
        else:
            return render(
            request,
            'account/register.html',
            {
                'title': 'Rejestracja',
                'form': form
            }
        )
    else:
        return render(
            request,
            'account/register.html',
            {
                'title': 'Rejestracja',
                'form': AccountUserCreationForm()
            }
        )

@login_required
def logout(request):
    auth.logout(request)
    return redirect('store:home')