from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from customer.forms import CustomerCreationForm, Contact_Form, UpdateProfile
from vendor.models import Category, Product
from cart.models import Order
from customer.models import CustomerProfile
from django.contrib.auth.decorators import login_required


def get_user_order(request):
    user_profile = get_object_or_404(CustomerProfile, Customer=request.user)
    ord = Order.objects.filter(owner=user_profile, is_ordered=True)
    if ord.exists():
        return ord
    return 0


def index(request):
    return render(request, 'customer/base.html')


def profile(request):
    a = request.user
    customer = CustomerProfile.objects.get(Customer=a)
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
        placed_order = get_user_order(request)
        context = {
            'form': form,
            'ContactForm': ContactForm,
            'ordre': placed_order
        }
        return render(request, 'customer/profile.html', context)


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


def search_results(request):
    products = []
    current_order_products = []
    query = request.GET.get('q')
    # print(query)
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


def list_categories(request):
    categories = Category.objects.all()
    return render(request, 'customer/index.html', {'categories': categories})


def customer_signup(request):
    if request.method == 'POST':
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            contact_number = form.cleaned_data['contact_number']
            c = CustomerProfile.objects.get(Customer=user)
            c.phone_number = contact_number
            login(request, user)
            return redirect('customer:home')
    else:
        form = CustomerCreationForm()
    return render(request, 'customer/signup.html', {'form': form})


def customer_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('customer:home')
    else:
        form = AuthenticationForm
    return render(request, 'customer/login.html', {'form': form})


@login_required
def customer_logout(request):
    logout(request)
    return render(request, 'customer/logout.html')


def forgot_pass(request):
    return render(request, 'registration/password_reset_form.html')
