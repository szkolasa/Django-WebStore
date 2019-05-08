from django.core import serializers
from django.http import HttpRequest, JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.db.models import F

from store_admin.models import Category, Product
from profile.models import Address
from store.models import Cart

from store.forms import OrderForm

# Create your views here.

def home(request):
    assert isinstance(request, HttpRequest)
    products = Product.objects.order_by(F('id').desc()).all()[:16]

    return render(
        request,
        'store/home.html',
        {
            'title': 'Home',
            'products': products,
        }
    )

def menu(request):
    assert isinstance(request, HttpRequest)

    categories = list(((c.id, c.name) for c in Category.objects.filter(parent_category=None).all()))

    return JsonResponse(categories, safe=False)

def category(request, id):
    assert isinstance(request, HttpRequest)

    category = Category.objects.filter(id=id).first()
    subcategories = Category.objects.filter(parent_category=category).all()

    if subcategories:
        return render(
            request,
            'store/category.html',
            {
                'title': category.name,
                'categories': subcategories
            }
        )
    else:
        return redirect('/products/list/' + str(category.id))

def productlist(request, id):
    assert isinstance(request, HttpRequest)
    category = Category.objects.filter(id=id).first()

    if not category:
        return HttpResponseNotFound()

    products = Product.objects.filter(category=category)

    return render(
        request,
        'store/productList.html',
        {
            'title': category.name,
            'products': products
        }
    )

def product(request, id):
    assert isinstance(request, HttpRequest)
    product = Product.objects.filter(id=id).first()

    if not product:
        return HttpResponseNotFound()

    return render(
        request,
        'store/product.html',
        {
            'title': product.name,
            'product': product
        }
    )

def addtocart(request, id):
    assert isinstance(request, HttpRequest)
    product = Product.objects.filter(id=id).first()

    if not product:
        return HttpResponseNotFound()

    cart = Cart(request=request)
    cart.add(product)

    return redirect('store:cart')

def cart(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'store/cart.html',
        {
            'title': 'Koszyk',
        }
    )

def itemsincart(request):
    assert isinstance(request, HttpRequest)
    cart = Cart(request=request)
    return JsonResponse(cart.count(), safe=False)

def cartitems(request):
    assert isinstance(request, HttpRequest)
    cart = Cart(request=request)
    return JsonResponse(cart.cart, safe=False)

def productname(request, id=0):
    assert isinstance(request, HttpRequest)

    product = Product.objects.filter(id=id).first()

    if not product:
        return HttpResponseNotFound()

    return JsonResponse(product.name, safe=False)

def removeitem(request, id):
    assert isinstance(request, HttpRequest)

    cart = Cart(request=request)
    product = Product.objects.filter(id=id).first()
    cart.remove(product)

    return redirect('store:cart')

def incqty(request, id):
    assert isinstance(request, HttpRequest)

    product = Product.objects.filter(id=id).first()
    cart = Cart(request=request)
    cart.add(product)

    return redirect('store:cart')

def decqty(request, id):
    assert isinstance(request, HttpRequest)

    product = Product.objects.filter(id=id).first()
    cart = Cart(request=request)
    cart.add(product, -1)

    return redirect('store:cart')

def order(request):
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        form = OrderForm(user=request.user, data=request.POST)
        cart = Cart(request=request)
        if form.is_valid():
            form.save(cart=cart)
            cart.clear()
            return redirect('store:ordercreated')

        return render(
            request,
            'store/order.html',
            {
                'title': 'Dane do wysylki',
                'form': form,
            }
        )
    else:
        form = OrderForm(user=request.user)
        return render(
            request,
            'store/order.html',
            {
                'title': 'Dane do wysylki',
                'form': form,
            }
        )

def getaddress(request, id):
    assert isinstance(request, HttpRequest)

    if id > 0:
        address = Address.objects.filter(id=id).first()
        ret = serializers.serialize('json', [address, ])
        return JsonResponse(ret, safe=False)

    return JsonResponse('', safe=False)

def ordercreated(request):
    assert isinstance(request, HttpRequest)

    return render(
        request,
        'store/orderCreated.html',
        {
            'title': 'Zamowienie zostalo dodane',
        }
    )