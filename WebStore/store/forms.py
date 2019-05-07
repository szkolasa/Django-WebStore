from django import forms
from profile.models import Address

from django.utils.translation import ugettext_lazy as _

class OrderForm(forms.Form):
    choice_list = [(0, '')]

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

    address_list = forms.ChoiceField(choices=choice_list,
                                     widget=forms.Select({'class': 'form-control'}),
                                     required=False)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        if user.is_active:
            self.choice_list = [(0, '')] + list(((a.id, str(a.name)) for a in Address.objects.filter(user=user).all()))
            self.fields['address_list'].choices = self.choice_list