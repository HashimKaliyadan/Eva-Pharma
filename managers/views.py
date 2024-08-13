from django.shortcuts import get_object_or_404, render, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect

from main.functions import generate_form_errors
from main.decorators import allow_manager

from managers.models import Manager, Category, Product
from customers.models import Customer, Order
from managers.forms import CategoryForm, ProductForm


@login_required(login_url="/managers/login/")
@allow_manager
def index(request):

    orders=Order.objects.all().count()
    products=Product.objects.all().count()
    categories=Category.objects.all().count()
    customers=Customer.objects.all().count()

    instances=Order.objects.all()[:3]


    context = {
        "title": "EVA Restuarant Home",
        "orders":orders,
        "products":products,
        "categories":categories,
        "customers":customers,
        "instances":instances,
    }
    return render(request, 'manager/index.html', context=context)



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_manager:
                auth_login(request, user)

                return HttpResponseRedirect(reverse("managers:index"))
            else:
                context= {
                    "title": "Manager Login",
                    "error": True,
                    "message": "Invalid credentials or not allowed user"
                }
                return render(request, "manager/login.html", context=context)
        else:
            context= {
                "title": "Manager Login",
                "error": True,
                "message": "Invalid credentials or not allowed user"
            }
            return render(request, "manager/login.html", context=context)
    else:
        context= {
            "title" : "Manager Login"
        }
        return render(request, "manager/login.html", context=context)
    

def logout(request):
    auth_logout(request)

    return HttpResponseRedirect(reverse("managers:login"))
    

################################################################
################      CATEGORY        ##########################
################################################################


@login_required(login_url="/managers/login/")
@allow_manager
def category(request):
    instances = Category.objects.all()
    context = {
        "title": "EVA Restuarant Categories",
        "instances":instances,
    }
    return render(request, 'manager/categories.html', context=context)


@login_required(login_url="/managers/login/")
@allow_manager
def category_add(request):
    if request.method =="POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:category"))
        else:
            form = CategoryForm()
            context = {
                "title": "EVA Restuarant Add Categories",
                "error": True,
                "message": "Something went wrong",
                "form":form,
            }
            return render(request, 'manager/add-category.html', context=context)
    else:
        form = CategoryForm()
        context = {
            "title": "EVA Restuarant Add Categories",
            "form":form,
        }
        return render(request, 'manager/add-category.html', context=context)


@login_required(login_url="/managers/login/")
@allow_manager
def category_edit(request, id):
    instance =Category.objects.get(id=id)
    if request.method =="POST":
        form = CategoryForm(request.POST, request.FILES,instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:category"))
        else:
            form = CategoryForm(instance=instance)
            context = {
                "title": "EVA Restuarant Add Categories",
                "error": True,
                "message": "Something went wrong",
                "form":form,
            }
            return render(request, 'manager/add-category.html', context=context)
    else:
        form = CategoryForm(instance=instance)
        context = {
            "title": "EVA Restuarant Add Categories",
            "form":form,
        }
        return render(request, 'manager/add-category.html', context=context)



@login_required(login_url="/managers/login/")
@allow_manager
def category_delete(request, id):
    category = Category.objects.get(id=id)
    category.delete()

    return HttpResponseRedirect(reverse("managers:category"))



################################################################
################      PRODUCTS        ##########################
################################################################


@login_required(login_url="/managers/login/")
@allow_manager
def products(request):
    instances = Product.objects.all()
    context = {
        "title": "EVA Restuarant Products",
        "instances":instances,
    }
    return render(request, 'manager/products.html', context=context)


@login_required(login_url="/managers/login/")
@allow_manager
def products_add(request):
    if request.method =="POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:products"))
        else:
            form = ProductForm()
            context = {
                "title": "EVA Restuarant Add Product",
                "error": True,
                "message": "Something went wrong",
                "form":form,
            }
            return render(request, 'manager/add-product.html', context=context)
    else:
        form = ProductForm()
        context = {
            "title": "EVA Restuarant Add product",
            "form":form,
        }
        return render(request, 'manager/add-product.html', context=context)


@login_required(login_url="/managers/login/")
@allow_manager
def products_edit(request, id):
    instance =Product.objects.get(id=id)
    if request.method =="POST":
        form = ProductForm(request.POST, request.FILES,instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("managers:products"))
        else:
            form = ProductForm(instance=instance)
            context = {
                "title": "EVA Restuarant Edit Product",
                "error": True,
                "message": "Something went wrong",
                "form":form,
            }
            return render(request, 'manager/add-product.html', context=context)
    else:
        form = ProductForm(instance=instance)
        context = {
            "title": "EVA Restuarant Edit product",
            "form":form,
        }
        return render(request, 'manager/add-product.html', context=context)


@login_required(login_url="/managers/login/")
@allow_manager
def products_delete(request, id):
    prodcut = Product.objects.get(id=id)
    prodcut.delete()

    return HttpResponseRedirect(reverse("managers:products"))


@login_required(login_url="/managers/login/")
@allow_manager
def products_stock(request, id):
    prodcut = Product.objects.get(id=id)
    prodcut.is_stock=True
    prodcut.save()

    return HttpResponseRedirect(reverse("managers:products"))


@login_required(login_url="/managers/login/")
@allow_manager
def products_out(request, id):
    prodcut = Product.objects.get(id=id)
    prodcut.is_stock=False
    prodcut.save()

    return HttpResponseRedirect(reverse("managers:products"))


################################################################
################      CUSTOMER AND ORDERS        ###############
################################################################

@login_required(login_url="/managers/login/")
@allow_manager
def customers(request):
    instances = Customer.objects.all()
    context = {
        "title": "EVA Restuarant Customers",
        "instances":instances,
    }
    return render(request, 'manager/customers.html', context=context)


@login_required(login_url="/managers/login/")
@allow_manager
def orders(request):
    instances = Order.objects.all()
    context = {
        "title": "EVA Restuarant Orders",
        "instances":instances,
    }
    return render(request, 'manager/orders.html', context=context)


@login_required(login_url="/managers/login/")
@allow_manager
def orders_packed(request, id):
    pass


@login_required(login_url="/managers/login/")
@allow_manager
def orders_shipped(request, id):
    pass


@login_required(login_url="/managers/login/")
@allow_manager
def orders_delivered(request, id):
    pass