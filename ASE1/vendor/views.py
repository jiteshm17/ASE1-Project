from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from vendor.forms import VendorCreationForm, ProductsAdd
from vendor.models import VendorProfile, Product
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    return HttpResponse('Dear vendor, Welcome to the home page!')


def index(request):
    return render(request, 'vendor/base.html')


@login_required(login_url='vendor:login')
def add_products(request):
    if request.method == 'POST':
        form = ProductsAdd(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'vendor/modify_product.html')
    else:
        form_add = ProductsAdd()
    return render(request, 'vendor/add_products.html', {'form': form_add})


# To display items whose qty is less than 50

def view_products(request):
    products = Product.objects.all()
    return render(request, 'vendor/view_products.html', {'products': products})


def modify_products(request):
    pass


def vendor_signup(request):
    if request.method == 'POST':
        form = VendorCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            contact_number = form.cleaned_data['contact_number']
            # new_vendor = VendorProfile(Vendor=user,phone_number=contact_number)
            VendorProfile.objects.create(Vendor=user, phone_number=contact_number)

            send_mail('Hello vendor', 'Thanks for registering', settings.EMAIL_HOST_USER, [user.email], fail_silently=True)
            login(request, user)
            return redirect('vendor:view_products')
    else:
        form = VendorCreationForm()
    return render(request, 'vendor/signup.html', {'form': form})


def vendor_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('vendor:view_products')
    else:
        form = AuthenticationForm
    return render(request, 'vendor/login.html', {'form': form})


def vendor_logout(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'vendor/logout.html')
    else:
        return HttpResponse('Cannot hard code logout')