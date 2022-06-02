import random

from django.shortcuts import render, get_object_or_404

from mainapp.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache
from django.conf import settings
from django.views.decorators.cache import cache_page, never_cache


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category {pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product {pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = 'products_in_category_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category=pk, is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    products = Product.objects.all()

    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk).order_by('price')

    return same_products


@cache_page(3600)
def products(request, pk=None, page=1):
    title = "Каталог"
    links_menu = get_links_menu()
    products = get_products_ordered_by_price()

    if pk is not None:
        if pk == 0:
            products = get_products_ordered_by_price()
            category = {'name': 'все'}
        else:
            category = get_category(pk)
            products = get_products_in_category_ordered_by_price(pk)

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products,
        }

        return render(request, 'mainapp/products.html', context)

    hot_product = get_hot_product()
    same_product = get_same_products(hot_product)

    paginator = Paginator(products, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'links_menu': links_menu,
        'products': products_paginator,
        'hot_product': hot_product,
        'same_products': same_product,
    }

    return render(request, 'mainapp/products.html', context=context)

@never_cache
def product(request, pk):
    title = "детали продукта"
    links_menu = get_links_menu()
    product = get_product(pk)

    hot_product = get_hot_product()
    same_product = get_same_products(hot_product)

    context = {
        'title': title,
        'links_menu': links_menu,
        'product': product,
        'same_products': same_product,
    }

    return render(request, 'mainapp/product.html', context=context)