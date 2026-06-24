from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.contrib import messages
# from django.utils.decorators import method_decorator
from .forms import UserRegistrationForm

from .models import User

# --- REGISTRATION VIEW ---
def register_view(request):
   
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            messages.success(request, f"Welcome to the Invoice System, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please check the form below.")
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


# --- LOGIN VIEW ---
def login_view(request):
   
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            messages.success(request, f"Hello {user.username}, you are now logged in.")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})


# --- LOGOUT VIEW ---
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, "You have been successfully logged out.")
        return redirect('login')
    return render(request, 'accounts/logout.html')



@login_required 
def home_view(request):   
    return render(request, 'accounts/home.html')


class ProtectedView(LoginRequiredMixin, View):
    def get(self, request):
        staff_list = User.objects.all()
        return render(request, 'accounts/protected.html', {'staff_list': staff_list})