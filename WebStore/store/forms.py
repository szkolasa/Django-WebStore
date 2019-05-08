from django import forms
from profile.models import Address
from store.models import Cart, Order, OrderItem

from django.utils.translation import ugettext_lazy as _

class OrderForm(forms.Form):
    choice_list = [(0, '')]

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

    def save(self, cart):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        street = self.cleaned_data.get('street')
        house_number = self.cleaned_data.get('house_number')
        flat_number = self.cleaned_data.get('flat_number')
        zip_code = self.cleaned_data.get('zip_code')
        phone_number = self.cleaned_data.get('phone_number')
        city = self.cleaned_data.get('city')

        order = Order()
        order.first_name = first_name
        order.last_name = last_name
        order.street = street
        order.house_number = house_number
        order.flat_number = flat_number
        order.zip_code = zip_code
        order.phone_number = phone_number
        order.city = city
        order.user = self.user
        order.save()

        for item in cart:
            order_item = OrderItem()
            order_item.order = order
            order_item.product = item['product']
            order_item.price = item['price']
            order_item.quantity = item['quantity']
            order_item.save()


