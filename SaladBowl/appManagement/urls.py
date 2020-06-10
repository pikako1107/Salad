from . import views
import appManagement.views
from django.urls import path, include

urlpatterns = [
    path('', appManagement.views.index, name='index'),
]

