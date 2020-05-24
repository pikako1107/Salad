"""
Definition of urls for SaladBowl.
"""

from datetime import datetime
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView

from appProducts import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('appProducts/', include('appProducts.urls')),
    path('', views.MyLoginView.as_view(), name="login"),
    path('logout/', views.MyLogoutView.as_view(), name="logout"),
]