from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseNotFound, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

from store_admin.models import Category, Product
from store_admin.forms import AdminUserEditForm, AdminAddCategoryForm, AdminEditCategoryForm, AdminAddProductForm, AdminEditProductForm

from store.models import Order, OrderItem

# Create your views here.

def is_admin(user):
    return user.groups.filter(name='Admin').exists() or user.is_superuser

def is_employee(user):
    return user.groups.filter(Name='Employee').exists() or user.is_superuser

def is_special(user):
    return user.groups.all().exists() or user.is_superuser

@login_required
@user_passes_test(is_special)
def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'store_admin/home.html',
        {
            'title': 'Administracja'
        }
    )

@login_required
@user_passes_test(is_admin)
def users(request):
    assert isinstance(request, HttpRequest)
    users = User.objects.all()
    return render(
        request,
        'store_admin/users.html',
        {
            'title': 'Użytkownicy',
            'users': users,
        }
    )

@login_required
@user_passes_test(is_admin)
def deleteuser(request, id):
    assert isinstance(request, HttpRequest)
    user = User.objects.filter(id=id).first()

    if not user:
        return HttpResponseNotFound()

    if user.is_superuser:
        return HttpResponse('Unauthorized', status=401)

    user.delete()
    return redirect('store_admin:users')

@login_required
@user_passes_test(is_admin)
def edituser(request, id):
    assert isinstance(request, HttpRequest)

    user = User.objects.filter(id=id).first()

    if not user:
        return HttpResponseNotFound()

    if user.is_superuser:
        return HttpResponse('Access denied', staus=401)

    if request.method == 'POST':
        form = AdminUserEditForm(data=request.POST, id=id)

        if form.is_valid():
            form.save()
            return redirect('store_admin:users')

        return render(
            request,
            'store_admin/editUser.html',
            {
                'title': 'Edytuj użytkownika',
                'form': form
            }
        )

    form = AdminUserEditForm(id=id)

    return render(
        request,
        'store_admin/editUser.html',
        {
            'title': 'Edytuj użytkownika',
            'form': form
        }
    )

@login_required
@user_passes_test(is_special)
def categories(request):
    assert isinstance(request, HttpRequest)
    categories = Category.objects.all()
    return render(
        request,
        'store_admin/categories.html',
        {
            'title': 'Kategorie',
            'categories': categories
        }
    )

@login_required
@user_passes_test(is_special)
def addcategory(request):
    assert isinstance(request, HttpRequest)
    if request.method =='POST':
        form = AdminAddCategoryForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('store_admin:categories')

        return render(
            request,
            'store_admin/addCategory.html',
            {
                'title': 'Dodaj kategorie',
                'form': form
            }
        )
    else:
        form = AdminAddCategoryForm(user=request.user)
        return render(
            request,
            'store_admin/addCategory.html',
            {
                'title': 'Dodaj kategorie',
                'form': form
            }
        )

@login_required
@user_passes_test(is_special)
def editcategory(request, id):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = AdminEditCategoryForm(user=request.user, id=id, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('store_admin:categories')

        return render(
            request,
            'store_admin/editCategory.html',
            {
                'title': 'Edycja kategorii',
                'form': form
            }
        ) 
    else:
        form = AdminEditCategoryForm(user=request.user, id=id)
        return render(
            request,
            'store_admin/editCategory.html',
            {
                'title': 'Edycja kategorii',
                'form': form
            }
        )

@login_required
@user_passes_test(is_special)
def deletecategory(request, id):
    assert isinstance(request, HttpRequest)
    category = Category.objects.filter(id=id).first()

    if not category:
        return HttpResponseNotFound()

    category.delete()
    return redirect('store_admin:categories')

@login_required
@user_passes_test(is_special)
def products(request):
    assert isinstance(request, HttpRequest)
    products = Product.objects.all()
    return render(
        request,
        'store_admin/products.html',
        {
            'title': 'Produtky',
            'products': products
        }
    )

@login_required
@user_passes_test(is_special)
def addproduct(request):
    assert isinstance(request, HttpRequest)
    if request.method == 'POST':
        form = AdminAddProductForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            return redirect('store_admin:products')

        return render(
            request,
            'store_admin/addProduct.html',
            {
                'title': 'Dodaj produkt',
                'form': form
            }
        )
    else:
        form = AdminAddProductForm(user=request.user)
        return render(
            request,
            'store_admin/addProduct.html',
            {
                'title': 'Dodaj produkt',
                'form': form
            }
        )

@login_required
@user_passes_test(is_special)
def deleteproduct(request, id):
    assert isinstance(request, HttpRequest)
    product = Product.objects.filter(id=id).first()

    if not product:
        return HttpResponseNotFound()

    product.delete()
    return redirect('store_admin:products')

@login_required
@user_passes_test(is_special)
def editproduct(request, id):
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        form = AdminEditProductForm(user=request.user, id=id, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect('store_admin:products')

        return render(
            request,
            'store_admin/editProduct.html',
            {
                'title': 'Edytuj produkt',
                'form': form
            }
        )
    else:
        form = AdminEditProductForm(user=request.user, id=id)
        return render(
            request,
            'store_admin/editProduct.html',
            {
                'title': 'Edytuj produkt',
                'form': form
            }
        )

@login_required
@user_passes_test(is_special)
def orders(request):
    assert isinstance(request, HttpRequest)

    user = request.user
    orders = Order.objects.all()

    return render(
        request,
        'store_admin/orders.html',
        {
            'title': 'Zamowienia',
            'orders': orders
        }
    )

@login_required
@user_passes_test(is_special)
def orderdetails(request, id):
    assert isinstance(request, HttpRequest)

    order = Order.objects.filter(id=id).first()

    if not order:
        return HttpResponseNotFound()

    items = OrderItem.objects.filter(order = order).all()

    return render(
        request,
        'store_admin/orderDetails.html',
        {
            'title': 'Szczegoly zamowienia',
            'items': items
        }
    )