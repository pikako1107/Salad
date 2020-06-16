from . import views
import appWorks.views
from django.urls import path, include

urlpatterns = [
    path('works/', appWorks.views.works, name='works'),
    path('works/<int:num>', appWorks.views.works, name='works'),
    path('cast/', appWorks.views.cast, name='cast'),
    path('cast/<int:num>', appWorks.views.cast, name='cast'),
    path('progress/', appWorks.views.progress, name='progress'),
    path('progress/<int:num>', appWorks.views.progress, name='progress'),
    path('work_count/', appWorks.views.work_count, name='work_count'),
    path('work_count/<int:num>', appWorks.views.work_count, name='work_count'),
    #path('<page>/edit/<int:id>', appWorks.views.edit, name='edit'),
    #path('<page>/delete/<int:id>', appWorks.views.delete, name='delete'),
]
