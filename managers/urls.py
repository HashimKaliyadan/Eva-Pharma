from django.urls import path

from managers import views


app_name = "managers"

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),

    path('category/', views.category, name="category"),
    path('category/add/', views.category_add, name="category_add"),
    path('category/edit/<int:id>/', views.category_edit, name="category_edit"),
    path('category/delete/<int:id>/', views.category_delete, name="category_delete"),

    path('products/', views.products, name="products"),
    path('products/add/', views.products_add, name="products_add"),
    path('products/edit/<int:id>/', views.products_edit, name="products_edit"),
    path('products/delete/<int:id>/', views.products_delete, name="products_delete"),
    path('products/stock/<int:id>/', views.products_stock, name="products_stock"),
    path('products/out/<int:id>/', views.products_out, name="products_out"),

    path('customers/', views.customers, name="customers"),

    path('orders/', views.orders, name="orders"),
    path('orders/packed/<int:id>/', views.orders_packed, name="orders_packed"),
    path('orders/shipped/<int:id>/', views.orders_shipped, name="orders_packed"),
    path('orders/delivered/<int:id>/', views.orders_delivered, name="orders_delivered"),

]