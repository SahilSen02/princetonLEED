"""princetonhack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

import dashboard
from dashboard import views as dashboard_views
urlpatterns = [
    path("admin/", admin.site.urls, name='admin'),
    path("dashboard/", include('dashboard.urls')),
    path("", dashboard_views.index, name='homepage'),
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='dashboard/logout.html'), name='logout'),
    path('lookup/', dashboard_views.lookup, name='lookup'),
    path('notfound/', dashboard_views.notfound, name='notfound'),
    path('rankings/', dashboard_views.rankings, name='rankings')
]
