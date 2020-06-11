from . import views
import appMoney.views
from django.urls import path, include

urlpatterns = [
    path('blance/', appMoney.views.blance, name='blance'),
    path('blance/<int:num>', appMoney.views.blance, name='blance'),
    path('<page>/edit/<int:id>', appMoney.views.edit, name='edit'),
    path('<page>/delete/<int:id>', appMoney.views.delete, name='delete'),
    path('payment_create/', appMoney.views.payment_create, name='payment_create'),
    path('payment_search/', appMoney.views.payment_search, name='payment_search'),
    path('works_sum/', appMoney.views.works_sum, name='works_sum'),
]

