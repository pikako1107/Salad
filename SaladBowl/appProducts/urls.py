from . import views
import appProducts.views
from django.urls import path, include

urlpatterns = [
    path('', appProducts.views.index, name='index'),
    path('products/', appProducts.views.products, name='products'),
    path('products/<int:num>', appProducts.views.products, name='products'),
    path('sets/', appProducts.views.sets, name='sets'),
    path('sets/<int:num>', appProducts.views.sets, name='sets'),
    path('sales/', appProducts.views.sales, name='sales'),
     path('sales/<int:num>', appProducts.views.sales, name='sales'),
    path('<page>/edit/<int:id>', appProducts.views.edit, name='edit'),
    path('<page>/delete/<int:id>', appProducts.views.delete, name='delete'),
]
