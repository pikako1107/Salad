from . import views
import appMoney.views
from django.urls import path, include

urlpatterns = [
    path('money/', appMoney.views.money, name='money'),
]

