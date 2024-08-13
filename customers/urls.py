from django.urls import path

from customers import views


app_name = "customers"

urlpatterns = [
    path('', views.index, name="index"),
    path('account/', views.account, name="account"),

    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),

    path('menu/', views.menu, name="menu"),
    path('cart/', views.cart, name="cart"),
    path('cart/add/<int:id>/', views.cart_add, name="cart_add"),
    path('cart/update/<int:id>/', views.cart_update, name="cart_update"),
    path('cart/remove/<int:id>/', views.cart_remove, name="cart_remove"),

    path('cart/update/page/<int:id>/', views.cart_update_page, name="cart_update_page"),
    path('cart/remove/page/<int:id>/', views.cart_remove_page, name="cart_remove_page"),
    path('order/place/', views.order_place, name="order_place"),

]