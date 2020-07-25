from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import createForm, deleteForm, postCommentForm, fileUploadForm
from .models import Room, Chat, File, Check
import datetime

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
    
    global message

    # メッセージ初期化
    message = ''

    # ログインユーザー取得
    user = request.user

    # POST送信判定
    if (request.method == 'POST'):
        # ボタン判定
        if 'comment' in request.POST:
            # コメント送信
            pass

        else:
            # ファイルアップロード
            # ファイルオブジェクト取得
            objFile = File()

            # データ取得
            objFile.uptime = datetime.datetime.today()          # アップロード日時
            objFile.roomID = id                                 # ルームID
            objFile.name = request.FILES['uploadplace'].name    # ファイル名

            # 確認期限
            chkDate = request.POST['deadlineDate']  

            # 日付チェック
            lineDate = checkDate(chkDate)

            # 日付不正の場合処理を抜ける
            if lineDate == '':
                message = "日付が不正のため、ファイルを登録できませんでした。"
                
            else:
                # フォームのインスタンス
                fileForm = fileUploadForm(request.POST, request.FILES, instance=objFile)

                if fileForm.is_valid(): 
                    # 保存
                    fileForm.save()

                    # メッセージ表示
                    message = "ファイルを登録しました。"

                else:
                    # エラーメッセージ表示
                    message = "ファイルを登録できませんでした。"

    # 確認状況データ取得

    params= {
        'title': name,
        'commentForm': postCommentForm,
        'fileForm':fileUploadForm,
        'user':user,
        'msg':message,
    }

    return render(request, 'appChat/chat.html', params)


''' 日付の妥当性チェック
    引数: strDate　入力値
    戻り値 正常:フォーマット変換した日付
           異常:空文字
'''
def checkDate(strDate):
    
    # 戻り値を初期化
    ans = ''

    try:
        # 日付を変換
        ans = datetime.datetime.strptime(strDate, '%Y-%m-%d')
        return ans

    except ValueError:
        return ans