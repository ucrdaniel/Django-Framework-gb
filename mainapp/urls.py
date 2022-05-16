from django.urls import path
from .views import products, product

app_name = 'mainapp'

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:pk>/', products, name='category'),
    path('category/page/<int:page>/', products, name='page'),
    path('<int:pk>/', product, name='detail'),
]