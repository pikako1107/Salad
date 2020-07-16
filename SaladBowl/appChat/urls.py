from . import views
import appChat.views
from django.urls import path, include

urlpatterns = [
    path('room/', appChat.views.room, name='room'),
    path('<name>/<int:id>', appChat.views.chat, name='chat'),
]


