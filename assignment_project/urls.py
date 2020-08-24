"""assignment_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from subscription.views import Subscriptions, Products
from users.views import Users, Login

urlpatterns = [
    path('api/subscriptions', csrf_exempt(Subscriptions.as_view())),
    path('api/products', csrf_exempt(Products.as_view())),
    path('api/users', csrf_exempt(Users.as_view())),
    path('api/login', csrf_exempt(Login.as_view())),
]
