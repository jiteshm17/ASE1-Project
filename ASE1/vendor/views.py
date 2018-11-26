from django.db.models import Q
from django.shortcuts import render, redirect
from cart.models import Order
from vendor.forms import ProductsAdd
from vendor.models import Product, Category, VendorProfile
from customer.forms import Contact_Form, UpdateProfile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from ASE1.decorators import vendor_required


def profile(request):
    a = request.user
    customer = VendorProfile.objects.get(Vendor=a)
    if request.method == 'POST':
        form = UpdateProfile(request.POST, instance=a)
        ContactForm = Contact_Form(request.POST, instance=customer)
        if form.is_valid() and ContactForm.is_valid():
            ph_no = ContactForm.cleaned_data.get('phone_number')
            addr = ContactForm.cleaned_data.get('address')
            user = form.save(commit=False)
            user.save()

            customer.phone_number = ph_no
            customer.address = addr
            customer.save()
            return redirect('customer:home')
    else:
        form = UpdateProfile(instance=request.user)
        ContactForm = Contact_Form(instance=customer)
        # placed_order = get_user_order(request)
        context = {
            'form': form,
            'ContactForm': ContactForm,
        }
        return render(request, 'vendor/profile.html', context)


def index(request):
    return render(request, 'vendor/base.html')


def items_view(request, pk):
    cat = Category.objects.get(id=pk)
    current_order_products = []
    if request.user.is_authenticated:
        filtered_orders = Order.objects.filter(owner=request.user.cus, is_ordered=False)
        if filtered_orders.exists():
            user_order = filtered_orders[0]
            user_order_items = user_order.items.all()
            current_order_products = [product.product for product in user_order_items]

    context = {
        'cat': cat,
        'current_order_products': current_order_products
    }

    return render(request, "customer/items.html", context)


def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'customer/index.html', {'categories': categories})


@login_required(login_url='vendor:actor_authentication:login_all')
@vendor_required
def add_products(request):
    if request.method == 'POST':
        form = ProductsAdd(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vendor:view_products')

    else:
        form = ProductsAdd()
    return render(request, 'vendor/add_products.html', {'form': form})


@login_required(login_url='vendor:actor_authentication:login_all')
@vendor_required
def view_products(request):
    product_list = Product.objects.all().order_by('prod_name')

    paginator = Paginator(product_list, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)
    return render(request, 'vendor/view_products.html', {'products': products})


@login_required(login_url='vendor:actor_authentication:login_all')
@vendor_required
def modify_products(request, id):
    product = Product.objects.get(pk=id)
    if request.method == 'POST':
        form = ProductsAdd(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('vendor:view_products')
    else:
        form = ProductsAdd(instance=product)
    return render(request, 'vendor/modify_product.html', {'form': form})


@login_required(login_url='vendor:actor_authentication:login_all')
@vendor_required
def delete_product(request, id):
    product = Product.objects.get(pk=id)
    name = product.prod_name
    product.delete()
    return render(request, 'vendor/deleted.html', {'name': name})


@login_required(login_url='vendor:actor_authentication:login_all')
@vendor_required
def view_orders(request):
    orders = Order.objects.filter(is_ordered=True)
    return render(request, 'vendor/show_orders.html', {'orders': orders})


def search_results(request):
    products = []
    current_order_products = []
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(
            Q(prod_name__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__cat_name__contains=query)
        )
    if request.user.is_authenticated:
        filtered_orders = Order.objects.filter(owner=request.user.cus)
        if filtered_orders.exists():
            user_order = filtered_orders[0]
            user_order_items = user_order.items.all()
            current_order_products = [product.product for product in user_order_items]
    context = {
        "products": products,
        "current_order_products": current_order_products,
    }
    return render(request, 'customer/search_results.html', context)
