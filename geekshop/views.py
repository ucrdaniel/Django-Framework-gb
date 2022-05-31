from django.shortcuts import render

from mainapp.models import Product


def index(request):
    products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:4]

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