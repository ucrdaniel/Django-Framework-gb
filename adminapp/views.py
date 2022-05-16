from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse, reverse_lazy

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/пользователи'
#
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     context = {
#         'title': title,
#         'objects': users_list
#     }
#
#     return render(request, 'adminapp/users.html', context)


class UsersListView(LoginRequiredMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    # context_object_name = 'objects'

    def get_context_data(self, **kwargs):
        context = super(UsersListView, self).get_context_data(**kwargs)
        context['title'] = 'админка/пользователи'

        return context


# @user_passes_test(lambda u: u.is_superuser)
# def user_create(request):
#     title = 'пользователи/создать'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin_stuff:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     context = {
#         'title': title,
#         'update_form': user_form
#     }
#
#     return render(request, 'adminapp/user_update.html', context)


class UserCreateView(LoginRequiredMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_stuff:users')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'админка/пользователи'

        return context


# @user_passes_test(lambda u: u.is_superuser)
# def user_update(request, pk):
#     title = 'пользователи/редактировать'
#
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin_stuff:user_update', args=[edit_user.pk]))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     context = {
#         'title': title,
#         'update_form': edit_form
#     }
#
#     return render(request, 'adminapp/user_update.html', context)

class UserUpdateView(UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_stuff:users')
    form_class = ShopUserAdminEditForm


# @user_passes_test(lambda u: u.is_superuser)
# def user_delete(request, pk):
#     title = 'пользователи/удалить'
#
#     user_to_delete = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         user_to_delete.is_active = False
#         user_to_delete.save()
#         return HttpResponseRedirect(reverse('admin_stuff:users'))
#
#     context = {
#         'title': title,
#         'user_to_delete': user_to_delete
#     }
#
#     return render(request, 'adminapp/user_delete.html', context)

class UserDeleteView(DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin_stuff:users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    context = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'adminapp/categories.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = 'категории/создание'

    if request.method == 'POST':
        edit_form = ProductCategoryEditForm(request.POST, request.FILES)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_stuff:categories'))
    else:
        edit_form = ProductCategoryEditForm()

    context = {
        'title': title,
        'update_form': edit_form
    }

    return render(request, 'adminapp/category_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = 'категории/редактирование'

    edit_category = get_object_or_404(ProductCategory, pk=pk)
    if request.method == 'POST':
        edit_form = ProductCategoryEditForm(request.POST, request.FILES, instance=edit_category)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_stuff:category_update', args=[edit_category.pk]))
    else:
        edit_form = ProductCategoryEditForm(instance=edit_category)

    context = {
        'title': title,
        'update_form': edit_form
    }

    return render(request, 'adminapp/category_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    title = 'категории/удалить'

    category_to_delete = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        category_to_delete.is_active = False
        category_to_delete.save()
        return HttpResponseRedirect(reverse('admin_stuff:categories'))

    context = {
        'title': title,
        'category_to_delete': category_to_delete
    }

    return render(request, 'adminapp/category_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def products(request, pk):
    title = 'админка/продукты'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    context = {
        'title': title,
        'category': category,
        'objects': products_list
    }

    return render(request, 'adminapp/products.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, pk):
    title = 'товары/создание'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_stuff:products', args=[pk]))
    else:
        edit_form = ProductEditForm(initial={'category': category})

    context = {
        'title': title,
        'update_form': edit_form,
        'category': category,
    }

    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    title = 'продукт/подробнее'
    product = get_object_or_404(Product, pk=pk)
    context = {
        'title': title,
        'object': product,
        'category': product.category,
    }

    return render(request, 'adminapp/product_read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    title = 'товары/рудактирование'
    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)

        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_stuff:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    context = {
        'title': title,
        'update_form': edit_form,
        'category': edit_product.category,
    }

    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    title = 'товары/удалить'

    product_to_delete = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product_to_delete.is_active = False
        product_to_delete.save()
        return HttpResponseRedirect(reverse('admin_stuff:products', args=[product_to_delete.category.pk]))

    context = {
        'title': title,
        'product_to_delete': product_to_delete,
        'category': product_to_delete.category,
    }

    return render(request, 'adminapp/product_delete.html', context)
