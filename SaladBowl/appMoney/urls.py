from . import views
import appMoney.views
from django.urls import path, include

urlpatterns = [
    path('blance/', appMoney.views.blance, name='blance'),
    path('blance/<int:num>', appMoney.views.blance, name='blance'),
    path('payment/', appMoney.views.payment, name='payment'),
    path('payment/<int:num>', appMoney.views.payment, name='payment'),
    path('payment_detail/', appMoney.views.payment_detail, name='payment_detail'),
    path('payment_detail/<int:num>', appMoney.views.payment_detail, name='payment_detail'),
    path('works_sum/', appMoney.views.works_sum, name='works_sum'),
    path('works_sum/<int:num>', appMoney.views.works_sum, name='works_sum'),
    path('<page>/edit/<int:id>', appMoney.views.edit, name='edit'),
    path('<page>/delete/<int:id>', appMoney.views.delete, name='delete'),
]

