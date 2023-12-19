from platformaDoKursow.helpers.allowed_methods_decorator import allowed_methods
from platformaDoKursow.forms.login_form import LoginForm, RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

@allowed_methods('GET,POST')
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('courses')
            else:
                messages.error(request, 'Invalid login params.')
    else:
        form = LoginForm()

    return render(request, 'login/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@allowed_methods('GET,POST')
def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Konto zostało utworzone. Możesz się teraz zalogować.')
            return redirect('courses')
    else:
        form = RegistrationForm()

    return render(request, 'login/registration.html', {'form': form})

def login_redirect(request):
    return redirect('login')
