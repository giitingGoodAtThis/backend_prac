from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

# Home page with login/signup popup
def myweb(request):
    return render(request, 'accounts/myweb.html')


# Dashboard page (requires login)
@login_required(login_url='/')
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'user': request.user})


# Logout API
# @csrf_exempt
# @require_http_methods(["POST"])
# def logout_view(request):
#     logout(request)
#     return JsonResponse({'status': 'success', 'message': 'Logged out'})
# Logout
def logout_view(request):
    logout(request)
    return redirect('myweb')  # redirect back to homepage

# Login API
@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Login successful'})
        return JsonResponse({'status': 'error', 'message': 'Invalid username or password'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


# Signup API
@csrf_exempt
@require_http_methods(["POST"])
def signup_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            return JsonResponse({'status': 'error', 'message': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email already exists'})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return JsonResponse({'status': 'success', 'message': 'Sign up successful'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
