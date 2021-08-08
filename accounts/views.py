from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, LoginForm, UserUpdateForm, ProfileUpdateForm

def register_user(request):
    context = {}
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            form.save()
            user = authenticate(username=username, password = raw_password)
            login(request, user)
            messages.success(request, f"Account created successfully! Welcome {user.first_name} ")
            return redirect('home')
        
    else:
        form = SignUpForm()
    context['form'] = form
    return render(request, 'accounts/signup.html', context)


def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            try:
                username = User.objects.filter(email=form.cleaned_data['email']).first().username
                password = form.cleaned_data['password']
                user = authenticate(username=username, password = password)
                if user:
                    login(request, user)
                    messages.success(request, f"Welcome back,  {user.first_name.capitalize() +' '+ user.last_name.capitalize()}")
                    return redirect('home')
                else:
                    form.add_error(field='password', error="Password is incorrect")
            except AttributeError:
                    form.add_error(field= 'email', error="Email is not registered")
            
    return render(request, 'accounts/login.html', {'form':form})


@login_required
def logout_user(request):
    logout(request)
    return redirect('home')


@login_required
def profile_user(request):
    return render(request, 'accounts/profile.html')


@login_required
def update_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance= request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance= request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance= request.user)
        p_form = ProfileUpdateForm(instance= request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'accounts/update_profile.html', context)