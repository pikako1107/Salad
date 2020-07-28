"""
Definition of urls for SaladBowl.
"""

from datetime import datetime
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

from appProducts import views
from appMoney import views
from appWorks import views
from appChat import views
from appManagement import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('appProducts/', include('appProducts.urls')),
    path('appMoney/', include('appMoney.urls')),
    path('appWorks/', include('appWorks.urls')),
    path('appChat/', include('appChat.urls')),
    path('appManagement/', include('appManagement.urls')),
    path('', views.MyLoginView.as_view(), name="login"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)