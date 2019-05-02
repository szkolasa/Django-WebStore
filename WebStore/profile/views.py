from django.http import HttpRequest, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from profile.forms import AccountChangePasswordForm, AccountChangeEmailForm, AccountShipmentForm, AccountEditShipmentForm
from profile.models import Address

# Create your views here.

@login_required
def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'profile/home.html',
        {
            'title': 'Konto'
        }
    )

@login_required
def changePassword(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = AccountChangePasswordForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return render(
                request,
                'profile/changePassword.html',
                {
                    'title': 'Zmiana hasla',
                    'form': AccountChangePasswordForm(user=request.user),
                    'message': 'Haslo zostalo zmienione'
                }
            )
        else:
            return render(
                request,
                'profile/changePassword.html',
                {
                    'title': 'Zmiana hasla',
                    'form': form
                }
            )
    else:
        form = AccountChangePasswordForm(user=request.user)
        return render(
            request,
            'profile/changePassword.html',
            {
                'title': 'Zmiana hasla',
                'form': form
            }
        )

@login_required
def changeemail(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = AccountChangeEmailForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return render(
                request,
                'profile/changeEmail.html',
                {
                    'title': 'Zmien email',
                    'form': AccountChangeEmailForm(user=request.user),
                    'message': 'Email zostal zmieniony'
                }
            )

        return render(
            request,
            'profile/changeEmail.html',
            {
                'title': 'Zmien email',
                'form': form,
            }
        )
    else:
        form = AccountChangeEmailForm(user=request.user)
        return render(
            request,
            'profile/changeEmail.html',
            {
                'title': 'Zmien email',
                'form': form
            }
        )

@login_required
def shipments(request):
    assert isinstance(request, HttpRequest)
    shipments = Address.objects.filter(user=request.user.id)
    return render(
        request,
        'profile/shipments.html',
        {
            'title': 'Dostawa',
            'shipments': shipments
        }
    )

@login_required
def addshipment(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = AccountShipmentForm(user=request.user, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('profile:shipments')
        else:
            return render(
            request,
                'profile/addShipment.html',
                {
                    'title': 'Nowy adres dostawy',
                    'form': form
                }
            )
    else:
        form = AccountShipmentForm(user=request.user)
        return render(
            request,
            'profile/addShipment.html',
            {
                'title': 'Nowy adres dostawy',
                'form': form
            }
        )

@login_required
def deleteshipment(request, id):
    assert isinstance(request, HttpRequest)
    shipment = Address.objects.filter(id=id)

    if shipment:
        shipment.delete()
        return redirect('profile:shipments')
    else:
        return HttpResponseNotFound()

@login_required
def editshipment(request, id):
    assert isinstance(request, HttpRequest)
    shipment = Address.objects.filter(id=id)

    if shipment:
        if request.method == 'POST':
            form = AccountEditShipmentForm(user=request.user, id=id, data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('profile:shipments')
            return render(
                request,
                'profile/editShipment.html',
                {
                    'title': 'Edytuj adres',
                    'form': form
                }
            )
        else:
            form = AccountEditShipmentForm(user=request.user, id=id)
            return render(
                request,
                'profile/editShipment.html',
                {
                    'title': 'Edytuj adres',
                    'form': form
                }
            )
    else:
        return HttpResponseNotFound()