from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import createForm, deleteForm, postCommentForm
from .models import Room, Chat, File, Check

# グローバル変数
message = ''

# Create your views here.
# ルーム選択ページ表示
@login_required
def room(request):

    global message

    # メッセージ初期化
    message = ''

    # POST送信判定
    if (request.method == 'POST'):
        # ボタン判定
        if 'input' in request.POST:
            # 作成ボタンクリック
            # インスタンス作成
            insertData = Room(
                               name = request.POST['roomName']
                                )

            # 保存
            insertData.save()

            # メッセージ
            message = "ルームを作成しました。"

        else:
            # 削除ボタンクリック
            # 対象ID
            id = int(request.POST['roomName'])

            # オブジェクト取得
            objRoom = Room.objects.get(id = id)            # ルームテーブル
            objChat = Chat.objects.filter(roomID = id)     # チャットテーブル
            objFile = File.objects.filter(roomID = id)     # ファイルテーブル

            # ルームデータ削除
            objRoom.delete()

            if objChat != '':
                # チャットデータ削除
                objChat.delete()

            if objFile != '':
                # ファイルデータ削除
                objFile.delete()

            # メッセージ
            message = "ルームを削除しました。"

    # ルームデータ取得
    data = Room.objects.all()

    params= {
        'title':'さらぼー管理/チャットルーム',
        'msg':message,
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