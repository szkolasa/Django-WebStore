from django import forms
from django.contrib.auth.models import Group, User

from store_admin.models import Category, Product

import datetime
from decimal import Decimal

class AdminUserEditForm(forms.Form):
    choice_list = [(0, '')] + list(((g.id, str(g.name)) for g in Group.objects.all()))

    user_id = forms.CharField(widget=forms.HiddenInput())
    group = forms.ChoiceField(choices=choice_list,
                              widget=forms.Select({'class': 'form-control'}))

    username = forms.CharField(widget=forms.TextInput({'class': 'form-control', 'readonly': True}))

    def __init__(self, id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = id
        user = User.objects.filter(id=id).first()
        self.fields['user_id'].initial = id
        self.fields['username'].initial = user.username
        self.choice_list = [(0, '')] + list(((g.id, str(g.name)) for g in Group.objects.all()))
        self.fields['group'].choices = self.choice_list

    def save(self, commit=True):
        user = User.objects.filter(id=self.cleaned_data.get('user_id')).first()
        user.groups.clear()
        group_id = int(self.cleaned_data.get('group'))

        if commit:
            group = Group.objects.filter(id=group_id).first()
            group.user_set.add(user)
            
        return user

class AdminAddCategoryForm(forms.Form):
    choice_list = [(0, '')] + list(((c.id, str(c.name)) for c in Category.objects.all()))

    name = forms.CharField(widget=forms.TextInput({'class': 'form-control'}))
    parent_category = forms.ChoiceField(choices=choice_list,
        widget=forms.Select({'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.choice_list = [(0, '')] + list(((c.id, str(c.name)) for c in Category.objects.all()))
        self.fields['parent_category'].choices = self.choice_list

    def save(self, commit=True):
        name = self.cleaned_data.get('name')
        parent_category = int(self.cleaned_data.get('parent_category'))

        category = Category()
        category.name = name
        category.created_by = self.user

        if parent_category > 0:
            parent = Category.objects.filter(id=parent_category).first()
            category.parent_category = parent

        category.created_date = datetime.datetime.now()

        if commit:
            category.save()

        return category

class AdminEditCategoryForm(AdminAddCategoryForm):
    category_id = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, user, id, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        category = Category.objects.filter(id=id).first()
        
        if (category.id, category.name) in self.choice_list:
            self.choice_list.remove((category.id, category.name))

        self.fields['category_id'].initial = id
        self.fields['name'].initial = category.name

        if category.parent_category != None:
            self.fields['parent_category'].initial = category.parent_category.id

    def save(self, commit=True):
        id = int(self.cleaned_data.get('category_id'))
        category = Category.objects.filter(id=id).first()
        name = self.cleaned_data.get('name')
        parent = int(self.cleaned_data.get('parent_category'))
        
        category.name = name

        if parent == 0:
            category.parent_category = None
        else:
            category.parent_category = Category.objects.filter(id=parent).first()

        if commit:
            category.save()

        return category

class AdminAddProductForm(forms.Form):
    category_list = list((c.id, c.name) for c in Category.objects.exclude(parent_category=None).all())

    name = forms.CharField(widget=forms.TextInput({'class': 'form-control'}))
    price = forms.CharField(widget=forms.TextInput({'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea({'class': 'form-control'}))
    category = forms.ChoiceField(choices=category_list,
                                 widget=forms.Select({'class': 'form-control'}))

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.category_list = list((c.id, c.name) for c in Category.objects.exclude(parent_category=None).all())
        self.fields['category'].choices = self.category_list

    def save(self, commit=True):
        category_id = int(self.cleaned_data.get('category'))
        category = Category.objects.filter(id=category_id).first()
        name = self.cleaned_data.get('name')
        price = Decimal(self.cleaned_data.get('price'))

        product = Product()
        product.added_by = self.user
        product.category = category
        product.name = name
        product.price = price
        product.description = self.cleaned_data.get('description')

        if commit:
            product.save()

   
class AdminEditProductForm(AdminAddProductForm):
    product_id = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, user, id, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        product = Product.objects.filter(id=id).first()

        self.fields['product_id'].initial = id
        self.fields['name'].initial = product.name
        self.fields['category'].initial = product.category.id
        self.fields['price'].initial = product.price
        self.fields['description'].initial = product.description

    def save(self, commit=True):
        product_id = int(self.cleaned_data.get('product_id'))
        product = Product.objects.filter(id=product_id).first()

        product.name = self.cleaned_data.get('name')
        product.price = Decimal(self.cleaned_data.get('price'))
        product.description = self.cleaned_data.get('description')

        category_id = int(self.cleaned_data.get('category'))
        category = Category.objects.filter(id=category_id).first()

        product.category = category

        if commit:
            product.save()
