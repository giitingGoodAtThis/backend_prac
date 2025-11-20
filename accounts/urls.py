from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.myweb, name='myweb'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
]

