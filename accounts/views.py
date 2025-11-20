from django.shortcuts import render

# Create your views here.

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

# this renders your HTML page
def myweb(request):
    return render(request, 'accounts/myweb.html')  # login.html should be inside accounts/templates/

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