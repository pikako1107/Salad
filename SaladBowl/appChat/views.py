from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import createForm, deleteForm

# Create your views here.
# ルーム選択ページ表示
@login_required
def room(request):

    # POST送信判定
    if (request.method == 'POST'):
        pass

    params= {
        'title':'さらぼー管理/チャットルーム',
        'createForm':createForm,
        'deleteForm':deleteForm,
    }

    return render(request, 'appChat/room.html', params)