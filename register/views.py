from django.shortcuts import render
from register.forms import LoginForm,RegisterForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'register/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def register(request):

    registered = False

    if request.method == "POST":
        loginform = LoginForm(data=request.POST)
        registerform=RegisterForm(data=request.POST)

        if loginform.is_valid() and registerform.is_valid():

            user = loginform.save()
            user.set_password(user.password)
            user.save()

            profile =registerform.save(commit=False)
            profile.user =user

            profile.save()

            registered = True
        else:
            print(loginform.errors, registerform.errors)
    else:
        loginform = LoginForm()
        registerform = RegisterForm()

    return render(request,'register/registration.html',
                  {'loginform':loginform,
                   'registerform':registerform,
                   'registered':registered})

def login_user(request):

    if request.method=='POST':
        username =request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))

            else:
                return HttpResponse("Account Not Active")

        else:
            print("Login Failed")
            print("username:{} and password {} ".format(username,password))
            return HttpResponse("Invalid login details")

    else:
        return render(request,'register/login.html',{})




