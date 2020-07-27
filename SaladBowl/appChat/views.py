from django.shortcuts import render
from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from .forms import createForm, deleteForm, postCommentForm, fileUploadForm
from .models import Room, Chat, File, Check
from appManagement.models import User
import datetime
import os

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
            objCheck = Check.objects.filter(roomID = id)   # 確認状況テーブル

            # ファイル名取得
            for item in objFile:
                # ファイルのパスを取得
                path = settings.MEDIA_ROOT + '/' + str(item.uploadplace)
                
                # 対象ファイル削除
                os.remove(path)

            # ルームデータ削除
            objRoom.delete()

            if objChat != '':
                # チャットデータ削除
                objChat.delete()

            if objFile != '':
                # ファイルデータ削除
                objFile.delete()

            if objCheck != '':
                # 確認状況データ削除
                objCheck.delete()

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
    loginUser = request.user

    # POST送信判定
    if (request.method == 'POST'):
        # ボタン判定
        if 'comment' in request.POST:
            # コメント送信
            # データ取得
            # 投稿コメント
            requestComment = request.POST.getlist('comment') 
            commentInsert = requestComment[0]

            # ルームID
            roomIDInsert = id                       

            # ユーザー名(英語)
            userEnglishInsert = loginUser

            # ユーザー名(日本語)取得
            userInsert = getUser(request,  loginUser)                

            # 投稿日時
            timeInsert = datetime.datetime.today()  

            # インスタンス作成
            insertChat = Chat(
                                roomID = roomIDInsert,
                                user = userInsert,
                                userEnglish = userEnglishInsert,
                                posttime = timeInsert,
                                comment = commentInsert
                )

            # 保存
            insertChat.save()

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

                    # 最新のデータを取得
                    newData = File.objects.all().values('id','roomID').order_by('-uptime').first()

                    # 各IDを変数に格納
                    fileIDInsert = newData['id']
                    roomIDInsert = newData['roomID']

                    # ユーザーデータ取得
                    users = createCheck()

                    # 確認状況データ作成
                    for userInsert in users:
                        # インスタンス作成
                        insertCheck = Check(
                                            fileID = fileIDInsert,
                                            roomID = roomIDInsert,
                                            user = userInsert['name'],
                            )

                        # 保存
                        insertCheck.save()

                    # メッセージ表示
                    message = "ファイルを登録しました。"

                else:
                    # エラーメッセージ表示
                    message = "ファイルを登録できませんでした。"

    else:
        # GET送信
        # ボタン判定
        if 'check' in request.GET:
            # 確認ボタン押下
            updateCheck(request, loginUser, 0)

        elif 'checkNo'  in request.GET:
            # 期限内には無理ボタン押下
            updateCheck(request, loginUser, 1)
                            
    # 投稿データ取得
    dataChat = Chat.objects.filter(roomID=id).order_by('-posttime')

    # ファイルデータ取得
    dataFile = File.objects.filter(roomID=id).order_by('-uptime')

    # 確認状況データ取得
    dataCheck = Check.objects.filter(roomID=id).exclude(checkBool=0).order_by('id')

    params= {
        'title': name,
        'commentForm': postCommentForm,
        'fileForm':fileUploadForm,
        'user':loginUser,
        'msg':message,
        'dataChat':dataChat,
        'dataCheck':dataCheck,
        'dataFile':dataFile,
        'mediaPath':settings.MEDIA_ROOT
    }

    return render(request, 'appChat/chat.html', params)

# 画面処理以外の関数
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

''' 確認状況データ作成(ユーザー取得)
    戻り値 ユーザーデータ
'''
def createCheck():
    # ユーザー取得
    getUser = User.objects.exclude(EnglishName='').values('name')

    return getUser 

''' ユーザー名を取得
    引数: request
          loginName ログイン名
    戻り値 ユーザー名(日本語)
'''
def getUser(request, loginName):
        
    # ユーザー
    getObj = User.objects.values('name').get(EnglishName=loginName)

    return getObj['name']

''' 確認状況テーブル更新
    引数：request
          logUser   ログインユーザー(英語)      
          mode  0:確認済み
                1:期限内には無理
    戻り値：なし
'''
def updateCheck(request, logUser, mode):
    
    # ファイルID取得
    chkFileID = request.GET['fileID_dummy'] # ファイルID

    # ユーザー名(日本語)取得
    userName = getUser(request, logUser)

    if mode == 0:
        # 確認済み
        chkDate = datetime.datetime.today()     # 確認日付
        chkBool = True                          # 確認フラグ

    else:
        # 期限内には無理
        chkBool = False                         # 確認フラグ

    # 更新対象取得
    objChk = Check.objects.get(fileID=chkFileID, user=userName)

    # データ更新
    objChk.checkBool = chkBool  # 確認フラグ

    if mode == 0:
        objChk.checkdate = chkDate     # 確認日

    # 保存
    objChk.save()