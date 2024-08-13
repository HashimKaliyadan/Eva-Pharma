from django.shortcuts import get_object_or_404, render, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect

from django.db.models import Sum

from main.functions import generate_form_errors
from main.decorators import allow_customer

from managers.models import Manager, Category, Product
from customers.models import Customer, Order, OrderItem
from .forms import OrderForm, UserForm
from users.models import User


@login_required(login_url="/login/")
@allow_customer
def index(request):
    user=request.user
    categories = Category.objects.all()
    products = Product.objects.all()
    count = OrderItem.objects.filter(user=user, ordered=False).count()
    context = {
        "title": "EVA Restuarant Home",
        "categories": categories,
        "products": products,
        "count": count,
    }
    return render(request, 'customer/index.html', context=context)


@login_required(login_url="/login/")
@allow_customer
def account(request):
    user=request.user
    customer=Customer.objects.get(user=user)
    orders_count = Order.objects.filter(customer=customer).count()
    instances = Order.objects.filter(customer=customer)
    count = OrderItem.objects.filter(user=user, ordered=False).count()

    context = {
        "title": "EVA Restuarant Account",
        "user": user,
        "customer": customer,
        "orders_count": orders_count,
        "instances": instances,
        "count": count,
    }
    return render(request, 'customer/account.html', context=context)


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_customer:
                auth_login(request, user)

                return HttpResponseRedirect(reverse("customers:index"))
            else:
                context= {
                    "title": "Customer Login",
                    "error": True,
                    "message": "Invalid credentials or not allowed user"
                }
                return render(request, "customer/login.html", context=context)
        else:
            context= {
                "title": "Customer Login",
                "error": True,
                "message": "Invalid credentials or not allowed user"
            }
            return render(request, "customer/login.html", context=context)
    else:
        context= {
            "title" : "Manager Login"
        }
        return render(request, "customer/login.html", context=context)


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)

            user = User.objects.create_user(
                username = instance.username,
                password = instance.password,
                email = instance.email,
                first_name = instance.first_name,
                phone_number = instance.phone_number,
                is_customer=True
            )

            customer = Customer.objects.create(
                user=user,
            )
            customer.save()

            user.save()

            return HttpResponseRedirect(reverse("customers:login"))
        else:
            message = generate_form_errors(form)
            form = UserForm()
            context= {
                "title": "Customer Register",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "customer/register.html", context=context)

    else:
        form = UserForm()
        context= {
            "title": "Customer. Register",
            "form": form,
        }
        return render(request, "customer/register.html", context=context)




def logout(request):
    auth_logout(request)

    return HttpResponseRedirect(reverse("customers:login"))


@login_required(login_url="/login/")
@allow_customer
def menu(request):
    user=request.user
    customer=Customer.objects.get(user=user)
    categories = Category.objects.all()
    products = Product.objects.all()
    count = OrderItem.objects.filter(user=user, ordered=False).count()
    context = {
        "title": "EVA Restuarant Home",
        "categories": categories,
        "products": products,
        "count": count,
    }
    return render(request, 'customer/menu.html', context=context)


@login_required(login_url="/login/")
@allow_customer
def cart(request):
    user=request.user
    customer=Customer.objects.get(user=user)
    instances = OrderItem.objects.filter(user=user, ordered=False)
    count = OrderItem.objects.filter(user=user, ordered=False).count()
    context = {
        "title": "EVA Restuarant Home",
        "customer": customer,
        "instances": instances,
        "count": count,
    }
    return render(request, 'customer/cart.html', context=context)


@login_required(login_url="/login/")
@allow_customer
def cart_add(request,id):
    user=request.user
    customer=Customer.objects.get(user=user)
    product = Product.objects.get(id=id)
    cart = OrderItem.objects.create(
        user=user,
        product=product,
        amount=product.price,
        qty=1,
        ordered=False,
    )
    cart.save()

    return HttpResponseRedirect(reverse("customers:menu"))


@login_required(login_url="/login/")
@allow_customer
def cart_update(request,id):
    user=request.user
    cart = OrderItem.objects.get(id=id)
    cart.amount = cart.amount + cart.product.price
    cart.qty += 1
    cart.save()
    return HttpResponseRedirect(reverse("customers:menu"))


@login_required(login_url="/login/")
@allow_customer
def cart_remove(request,id):
    user=request.user
    cart = OrderItem.objects.get(id=id)
    cart.amount = cart.amount - cart.product.price
    cart.qty -= 1
    cart.save()

    if cart.qty == 0:
        cart.delete()

    return HttpResponseRedirect(reverse("customers:menu"))


@login_required(login_url="/login/")
@allow_customer
def cart_update_page(request,id):
    user=request.user
    cart = OrderItem.objects.get(id=id)
    cart.amount = cart.amount + cart.product.price
    cart.qty += 1
    cart.save()
    return HttpResponseRedirect(reverse("customers:cart"))


@login_required(login_url="/login/")
@allow_customer
def cart_remove_page(request,id):
    user=request.user
    cart = OrderItem.objects.get(id=id)
    cart.amount = cart.amount - cart.product.price
    cart.qty -= 1
    cart.save()

    if cart.qty == 0:
        cart.delete()

    return HttpResponseRedirect(reverse("customers:cart"))



@login_required(login_url="/login/")
@allow_customer
def order_place(request):
    user= request.user
    customer = Customer.objects.get(user=user)
    carts = OrderItem.objects.filter(user=user, ordered=False)
    total_amount = carts.aggregate(Sum("amount"))["amount__sum"]
    count = OrderItem.objects.filter(user=user, ordered=False).count()

    if request.method == "POST":

        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.amount=total_amount
            instance.customer = customer
            instance.status= 'pending'
            instance.save()

            for cart in carts:
                instance.items.add(cart)
                cart.ordered=True
                cart.save()
            
            return HttpResponseRedirect(reverse("customers:account"))
        else:
            form = OrderForm()
            context = {
                "title": "EVA Restuarant Edit Product",
                "error": True,
                "message": "Something went wrong",
                "carts":carts,
                "user":user,
                "total_amount":total_amount,
                "form":form,
                "count":count,
            }
            return render(request, "customer/order-place.html", context=context)
    
    else:
        form = OrderForm()
        context= {
            "title": "Canteen | Menu",
            "carts":carts,
            "user":user,
            "total_amount":total_amount,
            "form":form,
            "count":count,
        }
        return render(request, "customer/order-place.html", context=context)
