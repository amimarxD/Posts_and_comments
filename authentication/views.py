from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import RegistrationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login')
def home(request):
    return render(request, "authentication/home.html")

# def login_user(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect(reverse('auth:home'))
#         else:
#             return redirect(reverse("auth:login"))
        
    # return render(request, "registration/login.html")

def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('auth:home'),)
    else:
        form = RegistrationForm()

    return render(request, "registration/sign-up.html", {"form": form})