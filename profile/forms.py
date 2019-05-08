from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

from profile.models import Address

# Create your forms here.

class AccountChangePasswordForm(PasswordChangeForm):
    new_password1 = forms.CharField(label=_("NewPassword"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control'}))

    new_password2 = forms.CharField(label=_("ConfirmNewPassword"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control'}))

    old_password = forms.CharField(label=_("OldPassword"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control'}))

class AccountChangeEmailForm(forms.Form):
    error_messages = {
        'email_missmatch': _("Aktualny email nie nalezy do tego konta"),
        'password_missmatch': _("Haslo sie nie zgadza"),
        'username_in_use': _("Nazwa zajeta"),
    }

    old_email = forms.CharField(label=_("OldEmail"),
                                widget=forms.EmailInput({
                                    'class': 'form-control'
                                }))

    new_email = forms.CharField(label=_("NewEmail"),
                                widget=forms.EmailInput({
                                    'class': 'form-control'
                                }))

    password1 = forms.CharField(label=_("Password"),
                                strip=False,
                                widget=forms.PasswordInput({
                                  'class': 'form-control'
                                }))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_email(self):
        old_email = self.cleaned_data.get('old_email')
        new_email = self.cleaned_data.get('new_email')
        password1 = self.data['password1']

        if old_email and new_email:
            if old_email != self.user.username:
                raise forms.ValidationError(
                    self.error_messages['email_missmatch'],
                    code='email_missmatch',
                )

            if self.user.check_password(password1) == False:
                raise forms.ValidationError(
                    self.error_messages['password_missmatch'],
                    code='password_missmatch',
                )

            if User.objects.filter(username=new_email).exists():
                raise forms.ValidationError(
                    self.error_messages['username_in_use'],
                    code='username_in_use',
                )

        return new_email

    def save(self, commit=True):
        username = self.cleaned_data["new_email"]
        self.user.username = username
        if commit:
            self.user.save()
        return self.user

class AccountShipmentForm(forms.Form):
    name = forms.CharField(label=_("FirstName"),
                               widget=forms.TextInput({
                                   'class': 'form-control'}))

    first_name = forms.CharField(label=_("FirstName"),
                               widget=forms.TextInput({
                                   'class': 'form-control'}))

    last_name = forms.CharField(label=_("FirstName"),
                               widget=forms.TextInput({
                                   'class': 'form-control'}))

    street = forms.CharField(label=_("FirstName"),
                               widget=forms.TextInput({
                                   'class': 'form-control'}))

    house_number = forms.CharField(label=_("FirstName"),
                               widget=forms.TextInput({
                                   'class': 'form-control'}))

    flat_number = forms.CharField(label=_("FirstName"),
                                  required=False,
                                  widget=forms.TextInput({
                                       'class': 'form-control'}))

    zip_code = forms.CharField(label=_("FirstName"),
                               widget=forms.TextInput({
                                   'class': 'form-control'}))

    phone_number = forms.CharField(label=_("FirstName"),
                               widget=forms.NumberInput({
                                   'class': 'form-control'}))

    city = forms.CharField(label=_("City"),
                               widget=forms.TextInput({
                                   'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        address = Address()
        address.user = self.user
        address.name = self.cleaned_data.get('name')
        address.first_name = self.cleaned_data.get('first_name')
        address.last_name = self.cleaned_data.get('last_name')
        address.street = self.cleaned_data.get('street')
        address.house_number = self.cleaned_data.get('house_number')
        address.flat_number = self.cleaned_data.get('flat_number')
        address.zip_code = self.cleaned_data.get('zip_code')
        address.phone_number = self.cleaned_data.get('phone_number')
        address.city = self.cleaned_data.get('city')

        if commit:
            address.save()

        return address

class AccountEditShipmentForm(AccountShipmentForm):
    shipment_id = forms.CharField(widget=forms.HiddenInput())
    
    def __init__(self, user, id, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        address = Address.objects.filter(id=id).first()
        self.fields['shipment_id'].initial = id
        self.fields['name'].initial = address.name
        self.fields['first_name'].initial = address.first_name
        self.fields['last_name'].initial = address.last_name
        self.fields['street'].initial = address.street
        self.fields['house_number'].initial = address.house_number
        self.fields['flat_number'].initial = address.flat_number
        self.fields['zip_code'].initial = address.zip_code
        self.fields['phone_number'].initial = address.phone_number
        self.fields['city'].initial = address.city

    def save(self, commit=True):
        address = Address.objects.filter(id=self.cleaned_data.get('shipment_id')).first()
        address.name = self.cleaned_data.get('name')
        address.first_name = self.cleaned_data.get('first_name')
        address.last_name = self.cleaned_data.get('last_name')
        address.street = self.cleaned_data.get('street')
        address.house_number = self.cleaned_data.get('house_number')
        address.flat_number = self.cleaned_data.get('flat_number')
        address.zip_code = self.cleaned_data.get('zip_code')
        address.phone_number = self.cleaned_data.get('phone_number')
        address.city = self.cleaned_data.get('city')

        if commit:
            address.save()

        return address
