from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import createForm, deleteForm, postCommentForm
from .models import Room

# Create your views here.
# ルーム選択ページ表示
@login_required
def room(request):

    # POST送信判定
    if (request.method == 'POST'):
        # ボタン判定
        if 'input' in request.POST:
            # 作成ボタンクリック
            pass

        else:
            # 削除ボタンクリック
            pass

    # ルームデータ取得
    data = Room.objects.all()

    params= {
        'title':'さらぼー管理/チャットルーム',
        'createForm':createForm,
        'deleteForm':deleteForm,
        'data':data,
    }

    return render(request, 'appChat/room.html', params)

# チャットページ表示
@login_required
def chat(request, name, id):
    
    # 確認状況データ取得


    params= {
        'title': name,
        'commentForm': postCommentForm,
    }

    return render(request, 'appChat/chat.html', params)