from django.urls import path
from .views import CategoryList, CategoryCreate, CategoryUpdate, CategoryDelete, \
    ProductList, ProductCreate, ProductUpdate, ProductDelete

app_name = 'product'

urlpatterns = [
    path('category_view', CategoryList.as_view(), name="CategoryList"),
    path('category_create', CategoryCreate.as_view(), name="CategoryCreate"),
    path('category_update/<int:pk>', CategoryUpdate.as_view(), name="CategoryUpdate"),
    path('category_delete/<int:pk>', CategoryDelete.as_view(), name="CategoryDelete"),
    path('product_view', ProductList.as_view(), name="ProductList"),
    path('product_create', ProductCreate.as_view(), name="ProductCreate"),
    path('product_update/<int:pk>', ProductUpdate.as_view(), name="ProductUpdate"),
    path('product_delete/<int:pk>', ProductDelete.as_view(), name="ProductDelete"),
]
