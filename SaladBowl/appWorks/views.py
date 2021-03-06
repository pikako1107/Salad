from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Max
from appManagement.models import User
from .models import Works, Cast, Progress
from .forms import worksForm, searchWorksForm, worksModelForm, castForm, searchCastForm, castModelForm, searchProgressForm, progressModelForm

# グローバル変数
message = ''

# (True:検索、False:登録)
chk = True

# Create your views here.
# 作品ページ表示
@login_required
def works(request, num=1):

    global message
    global chk

    # リスト初期化(未完のものを表示)
    whereSQL = ["completion = '0'"]

    # POST送信判定
    if (request.method == 'POST'):
        # ボタン判定
        if 'input' in request.POST:
            # 登録関数呼び出し(作品テーブル)
            dictData = create(request, 0)

            # インスタンス作成
            insertData = Works(
                            title = dictData['title'],
                            writer = dictData['writer'],
                            editor = dictData['editor'],
                            illustrator = dictData['illustrator'],
                            animator = dictData['animator'],
                            completion = dictData['completion']
                            )

            # 保存
            insertData.save()

            # 登録関数呼び出し(進捗テーブル)
            dictPro = create(request, 2)

            # インスタンス作成
            insertPro = Progress(
                                workID = dictPro['workID'],
                                editPro = dictPro['editPro'],
                                illustPro = dictPro['illustPro'],
                                animaPro = dictPro['animaPro']
                                )

            # 保存
            insertPro.save()

            message = "データを登録しました。"

        else:
            # 検索処理
            whereSQL = search(request, 0)
            # メッセージ初期化
            message = ''


    # データ抽出SQL作成
    sql =  "SELECT "
    sql += "        id, "
    sql += "        title, "
    sql += "        writer, "   
    sql += "        editor, "
    sql += "        illustrator, "
    sql += "        animator, "
    sql += "        CASE completion "
    sql += "            WHEN 1 THEN '完了' " 
    sql += "            ELSE '' "       
    sql += "        END AS completion "
    sql += "FROM "
    sql += "        appWorks_works "

    if whereSQL:
        # 条件を追加
        sql += ' WHERE '

        # ループをカウント
        i = 0

        for SQL in whereSQL:
            if i == 0:
                # ループ一回目
                sql += SQL
            else:
                # ループ二回目以降
                sql += 'AND ' + SQL

            # カウントアップ
            i += 1

    # 末尾にセミコロン追加
    sql += ';'

    # 作品テーブルデータ取得
    data = Works.objects.raw(sql)
    
    # ページネーション設定
    page = Paginator(data, 5)

    params= {
        'title':'さらぼー管理/作品',
        'type':'作品',
        'msg':message,
        'inputForm':worksForm(),
        'searchForm':searchWorksForm(),
        'data':page.get_page(num),
        'chk':chk,
    }

    if 'input' in request.POST:
        params['inputForm'] = worksForm(request.POST)
        
        # 登録ラジオボタンにチェック
        params['chk'] = False

    elif 'search' in request.POST:
        params['searchForm'] = searchWorksForm(request.POST)

        # 検索ラジオボタンにチェック
        params['chk'] = True

    return render(request, 'appWorks/works.html', params)

# キャストページ表示
@login_required
def cast(request, num=1):
    
    global message
    global chk

    # リスト初期化(未完のものを表示)
    whereSQL = ["status = '0'"]

    # POST送信判定
    if (request.method == 'POST'):
        # ボタン判定
        if 'input' in request.POST:
            # 登録関数呼び出し
            dictData = create(request, 1)

            # インスタンス作成
            insertData = Cast(
                            workID = dictData['workID'],
                            character = dictData['character'],
                            cast = dictData['cast'],
                            status = dictData['status']
                            )

            # 保存
            insertData.save()

            message = "データを登録しました。"

        else:
            # 検索処理
            whereSQL = search(request, 1)
            # メッセージ初期化
            message = ''


    # データ抽出SQL作成
    sql =  "SELECT "
    sql += "        c.id, "
    sql += "        w.title, "
    sql += "        c.character, "   
    sql += "        c.cast, "
    sql += "        CASE c.status "
    sql += "            WHEN 1 THEN '完了' " 
    sql += "            ELSE '収録中' "       
    sql += "        END AS status "
    sql += "FROM "
    sql += "        appWorks_cast AS c "
    sql += "INNER JOIN "
    sql += "        appWorks_works AS w "
    sql += "ON "
    sql += "        c.workID = w.id "

    if whereSQL:
        # 条件を追加
        sql += ' WHERE '

        # ループをカウント
        i = 0

        for SQL in whereSQL:
            if i == 0:
                # ループ一回目
                sql += SQL
            else:
                # ループ二回目以降
                sql += 'AND ' + SQL

            # カウントアップ
            i += 1

    # 末尾にセミコロン追加
    sql += ';'

    # キャストテーブルデータ取得
    data = Cast.objects.raw(sql)
    
    # ページネーション設定
    page = Paginator(data, 5)

    params= {
        'title':'さらぼー管理/キャスト',
        'type':'キャスト',
        'msg':message,
        'inputForm':castForm(),
        'searchForm':searchCastForm(),
        'data':page.get_page(num),
        'chk':chk,
    }

    if 'input' in request.POST:
        params['inputForm'] = castForm(request.POST)
        
        # 登録ラジオボタンにチェック
        params['chk'] = False

    elif 'search' in request.POST:
        params['searchForm'] = searchCastForm(request.POST)

        # 検索ラジオボタンにチェック
        params['chk'] = True

    return render(request, 'appWorks/cast.html', params)

# 進捗ページ表示
@login_required
def progress(request, num=1):
    
    global message
    global chk

    # リスト初期化(未完のものを表示)
    whereSQL = ["allPro <> 100"]

    # POST送信判定
    if (request.method == 'POST'):
        # 検索処理
        whereSQL = search(request, 2)
        # メッセージ初期化
        message = ''

    # データ抽出SQL作成
    sql =  "SELECT "
    sql += "        p.id, "       
    sql += "        p.workID, "
    sql += "        w.title, "
    sql += "        ifnull(((CAST(c2.完了数 AS REAL) / CAST(c1.全体個数 AS REAL)) * 100),0) AS castPro, "
    sql += "        w.editor, "   
    sql += "        CASE p.editPro "
    sql += "            WHEN 1 THEN '完了' "
    sql += "            ELSE '作業中' "
    sql += "        END AS editPro, "
    sql += "        w.illustrator, "
    sql += "        CASE p.illustPro "
    sql += "            WHEN 1 THEN '完了' "
    sql += "            ELSE '作業中' "
    sql += "        END AS illustPro, "
    sql += "        w.animator, "
    sql += "        CASE p.animaPro "
    sql += "            WHEN 1 THEN '完了' "
    sql += "            ELSE '作業中' "
    sql += "        END AS animaPro, "
    sql += "        ((ifnull((CAST(c2.完了数 AS REAL) / CAST(c1.全体個数 AS REAL) * 100),0) "
    sql += "        + (editPro * 100) "
    sql += "        + (illustPro * 100) "
    sql += "        + (animaPro * 100)) / 400) * 100 AS allPro "
    sql += "FROM "
    sql += "        appWorks_progress AS p "
    sql += "INNER JOIN "
    sql += "        appWorks_works AS w "
    sql += "ON "
    sql += "        p.workID = w.id "
    sql += "LEFT OUTER JOIN ("
    sql += "                SELECT "
    sql += "                    workID, "
    sql += "                    COUNT(*) AS 全体個数 "
    sql += "                FROM "
    sql += "                    appWorks_cast "
    sql += "                GROUP BY "
    sql += "                    workID) AS c1 "
    sql += "ON "
    sql += "                w.id = c1.workID "
    sql += "LEFT OUTER JOIN ("
    sql += "                SELECT "
    sql += "                    workID, "
    sql += "                    COUNT(*) AS 完了数 "
    sql += "                FROM "
    sql += "                    appWorks_cast "
    sql += "                WHERE "
    sql += "                    status = '1' "
    sql += "                GROUP BY "
    sql += "                    workID) AS c2 "
    sql += "ON "
    sql += "                w.id = c2.workID "               

    if whereSQL:
        # 条件を追加
        sql += ' WHERE '

        # ループをカウント
        i = 0

        for SQL in whereSQL:
            if i == 0:
                # ループ一回目
                sql += SQL
            else:
                # ループ二回目以降
                sql += 'AND ' + SQL

            # カウントアップ
            i += 1

    # 末尾にセミコロン追加
    sql += ';'

    # 進捗テーブルデータ取得
    data = Progress.objects.raw(sql)
    
    # ページネーション設定
    page = Paginator(data, 5)

    params= {
        'title':'さらぼー管理/進捗',
        'type':'進捗',
        'msg':message,
        'searchForm':searchProgressForm(),
        'data':page.get_page(num),
        'chk':chk,
    }

    if 'search' in request.POST:
        params['searchForm'] = searchProgressForm(request.POST)

        # 検索ラジオボタンにチェック
        params['chk'] = True

    return render(request, 'appWorks/progress.html', params)


# 作業集計ページ表示
@login_required
def work_count(request):
    
    # データ抽出SQL作成
    sql =  "SELECT "
    sql += "        u.id, "
    sql += "        u.name, "       
    sql += "        ifnull(p1.editPro, 0) AS editCnt, "
    sql += "        ifnull(p2.illustPro, 0) AS illustCnt, "
    sql += "        ifnull(p3.animaPro, 0) AS animaCnt, "
    sql += "        ifnull(c.castCnt, 0) AS castCnt, "
    sql += "        ifnull(p1.editPro, 0) "
    sql += "        + ifnull(p2.illustPro, 0) "
    sql += "        + ifnull(p3.animaPro, 0) "
    sql += "        + ifnull(c.castCnt, 0) AS allCnt "
    sql += "FROM "
    sql += "        appManagement_user AS u "
    sql += "LEFT OUTER JOIN ("
    sql += "                    SELECT "
    sql += "                            w.editor, "
    sql += "                            COUNT(*) AS editPro "
    sql += "                    FROM "
    sql += "                            appWorks_progress AS p "
    sql += "                    INNER JOIN "
    sql += "                            appWorks_works AS w "
    sql += "                    ON "
    sql += "                            p.workID = w.id "
    sql += "                    WHERE "
    sql += "                            p.editPro = 0 "
    sql += "                    GROUP BY "
    sql += "                            w.editor "
    sql += "                ) AS p1 "
    sql += "ON "
    sql += "    u.name = p1.editor "
    sql += "LEFT OUTER JOIN ("
    sql += "                    SELECT "
    sql += "                            w.illustrator, "
    sql += "                            COUNT(*) AS illustPro "
    sql += "                    FROM "
    sql += "                            appWorks_progress AS p "
    sql += "                    INNER JOIN "
    sql += "                            appWorks_works AS w "
    sql += "                    ON "
    sql += "                            p.workID = w.id "
    sql += "                    WHERE "
    sql += "                            p.illustPro = 0 "
    sql += "                    GROUP BY "
    sql += "                            w.illustrator "
    sql += "                ) AS p2 "
    sql += "ON "
    sql += "    u.name = p2.illustrator "
    sql += "LEFT OUTER JOIN ("
    sql += "                    SELECT "
    sql += "                            w.animator, "
    sql += "                            COUNT(*) AS animaPro "
    sql += "                    FROM "
    sql += "                            appWorks_progress AS p "
    sql += "                    INNER JOIN "
    sql += "                            appWorks_works AS w "
    sql += "                    ON "
    sql += "                            p.workID = w.id "
    sql += "                    WHERE "
    sql += "                            p.animaPro = 0 "
    sql += "                    GROUP BY "
    sql += "                            w.animator "
    sql += "                ) AS p3 "
    sql += "ON "
    sql += "    u.name = p3.animator "
    sql += "LEFT OUTER JOIN ("
    sql += "                    SELECT "
    sql += "                            c.cast, "
    sql += "                            COUNT(*) AS castCnt "
    sql += "                    FROM "
    sql += "                            appWorks_cast AS c "
    sql += "                    WHERE "
    sql += "                            c.status = 0 "
    sql += "                    GROUP BY "
    sql += "                            c.cast "
    sql += "                ) AS c "
    sql += "ON "
    sql += "    u.name = c.cast;"

    # 手持ち作業データ取得
    data = Progress.objects.raw(sql)

    params= {
        'title':'さらぼー管理/手持ち作業集計',
        'type':'手持ち作業集計',
        'data':data,
    }

    return render(request, 'appWorks/work_count.html', params)


# 編集ページ表示
@login_required
def edit(request, page, id):

    # 変数初期化
    info_message = 'ID:' + str(id) + 'のデータを編集します'
    type = ''

    # ページごとにテーブルを変更
    if page == 'works':
        obj = Works.objects.get(id = id)
        type = '作品'
        sent_form = worksModelForm(instance=obj)

    elif page == 'cast':
        obj = Cast.objects.get(id = id)
        type = 'キャスト'
        sent_form = castModelForm(instance=obj)

    else:
        obj = Progress.objects.get(id = id)
        type = '進捗'
        sent_form = progressModelForm(instance=obj)

    # POST送信判定
    if request.method == 'POST':
        # ページごとに処理変更
        if page == 'works':
            editData = worksModelForm(request.POST, instance=obj)
            editData.save()

        elif page == 'cast':
            editData = castModelForm(request.POST, instance=obj)
            editData.save()

        else:
            editData = progressModelForm(request.POST, instance=obj)
            editData.save()

        # メッセージを設定
        global message
        message = 'データを更新しました。'

        # リダイレクト
        return redirect(to='/appWorks/' + page)

    params = {
            'title':type + '更新',
            'info':info_message,
            'form':sent_form,
        }

    return render(request, 'appWorks/edit.html', params)


# 削除ページ表示
@login_required
def delete(request, page, id):
        
    # 変数初期化
    info_message = 'ID:' + str(id) + 'のデータを削除します'
    type = ''
    obj2 = ''

    # ページごとにテーブルを変更
    if page == 'works':
        obj = Works.objects.get(id = id)
        type = '作品'

        # 進捗・キャストデータも一緒に削除
        obj2 = Progress.objects.get(workID = id)
        obj3 = Cast.objects.filter(workID = id)

    elif page == 'cast':
        obj = Cast.objects.get(id = id)
        type = 'キャスト'

    # POST送信判定
    if request.method == 'POST':
        # データを削除
        obj.delete()

        if obj2 != '':
            # 進捗データ削除
            obj2.delete()

        if obj3 != '':
            # キャストデータ削除
            obj3.delete()

        # メッセージを設定
        global message
        message = 'データを削除しました。'

        # リダイレクト
        return redirect(to='/appWorks/' + page)

    params = {
            'title':type + '削除',
            'type':type,
            'info':info_message,
            'obj':obj,
        }

    return render(request, 'appWorks/delete.html', params)


# 画面処理以外の関数
''' 登録データ作成
    引数: request
          mode  0:作品テーブル更新
                1:キャストテーブル更新
                2:進捗テーブル更新
    戻り値 登録データ(辞書)
'''
def create(request, mode):

    if mode == 0:
        # 残高テーブル登録データ
        # 作品名
        title = request.POST['title']

        # 脚本検索
        writer = getUser(request, 'writer')

        # 編集検索
        editor = getUser(request, 'editor')

        # イラスト検索
        illustrator = getUser(request, 'illustrator')

        # 動画検索
        animator = getUser(request, 'animator')

        # 完了チェック
        if ('completion' in request.POST):
            # チェックありはTrue
            completion = True
        else:
            completion = False

        # 辞書に格納
        data = {'title':title, 
                'writer':writer, 
                'editor':editor, 
                'illustrator':illustrator, 
                'animator':animator,
                'completion':completion}

    elif mode == 1:
        # キャストテーブル更新データ
        # タイトルID
        workID = request.POST['workID']

        # キャラクター
        character = request.POST['character']

        # キャスト
        if request.POST['cast'] == '-1':
            # -1はゲスト
            cast = 'ゲスト'
        elif request.POST['cast'] == '-2':
            # -2は未定
            cast = '未定'
        else:
            cast = getUser(request, 'cast')

        # ステータス
        if ('status' in request.POST):
            # チェックありはTrue
            status = True
        else:
            status = False

        # 辞書に格納
        data = {'workID':workID, 
                'character':character, 
                'cast':cast, 
                'status':status}

    else:
        # 進捗テーブル更新データ
        # IDの最大値を取得
        maxID = Works.objects.aggregate(Max('id'))

        # タイトルID
        workID = maxID['id__max']

        # 進捗はすべて「作業中」で登録
        editPro = 0
        illustPro = 0
        animaPro = 0

        # 辞書に格納
        data = {'workID':workID, 
                'editPro':editPro, 
                'illustPro':illustPro, 
                'animaPro':animaPro}

    # 辞書を返す
    return data

''' データの検索
    引数: request
          mode  0:作品ページ検索
                1:キャストページ検索
    戻り値 WHERE句SQL(リスト)
'''
def search(request, mode): 
    # 戻り値の初期化
    ans = []

    # 変数初期化
    table = ""

    if mode == 0:
        # 作品テーブル検索       
        # 文字列はないのでダミー
        strData = {}

        # 数値はないのでダミー
        intData = {}

        # その他検索対象
        # タイトル検索(ID)
        if request.POST['title'] == '':
            # 未選択は検索しない
            id = ''
        else:
            id = request.POST['title']   

        # 脚本検索
        writer = getUser(request, 'writer')

        # 編集検索
        editor = getUser(request, 'editor')

        # イラスト検索
        illustrator = getUser(request, 'illustrator')

        # 動画検索
        animator = getUser(request, 'animator')

        # 完了チェック検索
        if request.POST['completion'] == '2':
            # 2は検索しない
            completion = ''
        else:
            completion = request.POST['completion']   


        # 辞書に格納{検索項目：検索値}
        eachData = {
                'id':id,
                'writer':writer,
                'editor':editor,
                'illustrator':illustrator,
                'animator':animator,
                'completion':completion,
                }

    elif mode == 1:
        # キャストテーブル検索
        table = "c."
        
        # 文字列検索対象
        charaWhere = request.POST['choiceChara']

        # 辞書に格納{検索項目：検索条件(0:完全一致、1:前方一致、2:後方一致)}
        strData = {
                'character':charaWhere,
            }

        # 数値はないのでダミー
        intData = {}

        # その他検索対象
        # タイトルID
        if request.POST['workID'] == '':
            # 未選択は検索しない
            workID = ''
        else:
            workID = request.POST['workID']

        # キャスト
        if request.POST['cast'] == '-1':
            # -1はゲスト
            cast = 'ゲスト'
        elif request.POST['cast'] == '-2':
            # -2は未定
            cast = '未定'
        elif request.POST['cast'] == '-3':
            # -3は検索しない
            cast = ''
        else:
            cast = getUser(request, 'cast')

        # ステータス
        if request.POST['status'] == '2':
            # 2は検索しない
            status = ''
        else:
            status = request.POST['status']  

        # 辞書に格納{検索項目：検索値}
        eachData = {
                'c.workID':workID,
                'c.cast':cast,
                'c.status':status,
                }

    else:
        # 進捗テーブル検索
        # 文字列はないのでダミー
        strData = {}

        # 数値検索対象
        castWhere = request.POST['choiceCastPro']    # 収録進捗検索条件
        allWhere = request.POST['choiceAllPro']      # 進捗率検索条件

        # 辞書に格納{検索項目：検索条件(0:一致、1:以上、2:以下)}
        intData = {
                'castPro':castWhere,
                'allPro':allWhere,
            }

        # その他検索対象
        # タイトルID
        if request.POST['workID'] == '':
            # 未選択は検索しない
            workID = ''
        else:
            workID = request.POST['workID']

        # 編集担当
        editor = getUser(request, 'editor')

        # 編集進捗
        if request.POST['editPro'] == '2':
            # 2は検索しない
            editPro = ''
        else:
            editPro = request.POST['editPro']

        # イラスト担当
        illustrator = getUser(request, 'illustrator')

        # イラスト進捗
        if request.POST['illustPro'] == '2':
            # 2は検索しない
            illustPro = ''
        else:
            illustPro = request.POST['illustPro']

        # 動画担当
        animator = getUser(request, 'animator')

        # 動画進捗
        if request.POST['animaPro'] == '2':
            # 2は検索しない
            animaPro = ''
        else:
            animaPro = request.POST['animaPro']

        # 辞書に格納{検索項目：検索値}
        eachData = {
                'p.workID':workID,
                'w.editor':editor,
                'editPro':editPro,
                'w.illustrator':illustrator,
                'illustPro':illustPro,
                'w.animator':animator,
                'animaPro':animaPro,
                }


    # 文字列検索SQL作成
    strSQL = strSearch(request, strData, table)

    # 数値検索SQL作成
    intSQL = intSearch(request, intData, table)

    # その他検索SQL作成
    eachSQL = eachSearch(eachData)

    # SQLリスト結合
    ans = strSQL + intSQL + eachSQL

    # 戻り値を設定
    return ans


''' データの検索(文字列)
    引数: request
          data　  文字列検索データ辞書
          table   メインに取得するテーブル
    戻り値 文字列検索SQL(リスト)
'''
def strSearch(request, data, table=''):
    # 戻り値の初期化
    ans = []

    # データ数分ループ
    for key in data:
        # 空文字(値が入力されていない)は飛ばす
        if request.POST[key] == '':
            continue
        else:
            # 検索条件により処理わけ
            if data[key] == '0':
                # 完全一致
                ans.append(table + key + " = '" + request.POST[key] + "' ")

            elif data[key] == '1':
                # 前方一致
                ans.append(table + key + " LIKE '" + request.POST[key] + "%' ")

            else:
                # 後方一致
                ans.append(table + key + " LIKE '%" + request.POST[key] + "' ")

    # 戻り値を設定
    return ans

''' データの検索(数値)
    引数: request
          data　  数値検索データ辞書
          table   メインに取得するテーブル
    戻り値 数値検索SQL(リスト)
'''
def intSearch(request, data, table=''):
    # 戻り値の初期化
    ans = []

    # データ数分ループ
    for key in data:
        # 空文字(値が入力されていない)は飛ばす
        if request.POST[key] == '':
            continue
        else:
            # 検索条件により処理わけ
            if data[key] == '0':
                # 一致
                ans.append(table + key + ' = ' + request.POST[key] + ' ')

            elif data[key] == '1':
                # 以上
                ans.append(table + key + ' >= ' + request.POST[key] + ' ')

            else:
                # 以下
                ans.append(table + key + ' <= ' + request.POST[key] + ' ')

    # 戻り値を設定
    return ans

''' データの検索(一致のみ)
    引数: data　検索データ辞書
    戻り値 検索SQL(リスト)
'''
def eachSearch(data):
    # 戻り値の初期化
    ans = []

    # データ数分ループ
    for key in data:
        # 空文字(値が入力されていない)は飛ばす
        if data[key] == '':
            continue
        else:
            # 値一致のみ
            ans.append(key + ' = "' + data[key] + '" ')

    # 戻り値を設定
    return ans

''' ユーザー名を取得
    引数: request
          field     検索項目
    戻り値 ユーザー名
           未選択の場合、空文字を返す
'''
def getUser(request, field):
    
    if request.POST[field] == '':
        # 空の場合処理を終了
        return ''

    # ユーザーID
    userID = request.POST[field] 
        
    # ユーザー
    getObj = User.objects.values('name').get(id=userID)

    return getObj['name']

''' 作品を取得
    引数: request
    戻り値 作品名
           未選択の場合、空文字を返す
'''
def getWork(request):

    if request.POST['works'] == '':
        # 空の場合処理を終了
        return ''

    # 作品ID
    workID = request.POST['works'] 
        
    # 作品名
    getObj = Works.objects.values('title').get(id=workID)

    return getObj['title']