from django.shortcuts import render

from basketapp.models import Basket
from mainapp.models import Product


def index(request):
    products = Product.objects.all()[:4]
    Product.objects.r

    context = {
        'title': 'главная',
        'products': products,
    }

    return render(request, 'geekshop/index.html', context)


def contacts(request):
    context = {
        'title': 'контакты',
    }
    return render(request, 'geekshop/contact.html', context)