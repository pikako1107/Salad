from django import forms
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Sum, Max
from django.contrib.auth.decorators import login_required
from .models import Pos, Payment, Payment_detail
from appManagement.models import User
from appWorks.models import Works
from .forms import posForm, searchPosForm, posModelForm, paymentDetailForm, paymentForm, searchPaymentForm, paymentModelForm, searchPaymentDetailForm, detailModelForm, worksSumForm
import datetime
import math

# Create your views here.

# グローバル変数
message = ''
money_1hour = 0

# (True:検索、False:登録)
chk = True

# 収支管理ページ表示
@login_required
def blance(request, num=1):

    global chk
    global message

    # リスト初期化
    whereSQL = []

    # POST送信判定
    if (request.method == 'POST'):
        # ボタン判定
        if 'input' in request.POST:
            # 登録関数呼び出し
            dictData = create(request, 0)

            # falseが戻ってきたら処理を抜ける
            if dictData != False:
                # インスタンス作成
                insertData = Pos(
                                posDate = dictData['posDate'],
                                blance = dictData['blance'],
                                user = dictData['user'],
                                money = dictData['money'],
                                note = dictData['note'],
                                paymentNo = dictData['paymentNo']
                                )

                # 保存
                insertData.save()

                message = "データを登録しました。"

        else:
            # 検索処理
            whereSQL = search(request, 0)
            # メッセージ初期化
            message = ''
    
    # データ抽出SQL作成
    sql = 'SELECT id, posDate, blance, user, money, note '
    sql += 'FROM appMoney_pos '

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

    # 残高テーブルデータ取得
    data = Pos.objects.raw(sql)
    
    # ページネーション設定
    page = Paginator(data, 5)

    # 残高算出
    sumPos = calcPos()

    # 列名
    col = ('ID', '日付', '収支', 'ユーザー', '金額', '備考')

    params= {
        'title':'さらぼー管理/収支',
        'type':'収支',
        'msg':message,
        'inputForm':posForm(),
        'searchForm':searchPosForm(),
        'data':page.get_page(num),
        'col':col,
        'sumPos':sumPos,
        'chk':chk,
    }

    if 'input' in request.POST:
        params['inputForm'] = posForm(request.POST)
        
        # 登録ラジオボタンにチェック
        params['chk'] = False

    elif 'search' in request.POST:
        params['searchForm'] = searchPosForm(request.POST)

        # 検索ラジオボタンにチェック
        params['chk'] = True

    return render(request, 'appMoney/blance.html', params)

# 立替金登録ページ表示
@login_required
def payment(request, num=1):

    global chk
    global message

    # リスト初期化
    whereSQL = []

    # POST送信判定
    if (request.method == 'POST'):
        # ボタン判定
        if 'input' in request.POST:
            # 登録関数呼び出し(立替金)
            dictData = create(request, 1)

            # falseが戻ってきたら処理を抜ける
            if dictData != False:
                # インスタンス作成(立替金)
                insertData = Payment(
                                    payDate = dictData['payDate'],
                                    place = dictData['place'],
                                    user = dictData['user'],
                                    money = dictData['money'],
                                    hour = dictData['hour'],
                                    money_1hour = dictData['money_1hour'],
                                    payoff = dictData['payoff'],
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
    sql = 'SELECT id, payDate, place, user, hour, money, money_1hour, payoff '
    sql += 'FROM appMoney_payment '

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

    # 立替金テーブルデータ取得
    data = Payment.objects.raw(sql)
    
    # ページネーション設定
    page = Paginator(data, 5)

    # 列名
    col = ('日付', '場所', 'ユーザー', '時間', '金額', '金額/1h', '精算チェック')  

    params= {
        'title':'さらぼー管理/立替金',
        'type':'立替金',
        'msg':message,
        'inputForm':paymentForm(),
        'searchForm':searchPaymentForm(),
        'data':page.get_page(num),
        'col':col,
        'sumPos':'',
        'chk':chk,
    }

    if 'input' in request.POST:
        params['inputForm'] = paymentForm(request.POST)

        # 登録ラジオボタンにチェック
        params['chk'] = False

    elif 'search' in request.POST:
        params['searchForm'] = searchPaymentForm(request.POST)

        # 検索ラジオボタンにチェック
        params['chk'] = True

    return render(request, 'appMoney/blance.html', params)

# 詳細登録ページ表示
@login_required
def payment_detail(request, num=1):

    global chk
    global message

    # リスト初期化
    whereSQL = []

    # POST送信判定
    if (request.method == 'POST'):
        # ボタン判定
        if 'input' in request.POST:
            # 登録関数呼び出し(立替金詳細)
            dictData = create(request, 2)

            # インスタンス作成(立替金詳細)
            insertData = Payment_detail(
                                        activity_id = dictData['activity_id'],
                                        content = dictData['content'],
                                        work_id = dictData['work_id'],
                                        hour = dictData['hour'],
                                        money = dictData['money'],
                                        )

            # 保存
            insertData.save()

            message = "データを登録しました。"

        else:
            # 検索処理
            whereSQL = search(request, 2)

            # メッセージ初期化
            message = ''

    # データ抽出SQL作成
    sql =  "SELECT p.payDate, "
    sql += "pd.id, "
    sql += "CASE p.place "
    sql += "	WHEN 0 THEN '会議室'"
    sql += "	WHEN 1 THEN 'スタジオ'"
    sql += "END AS place, "
    sql += "CASE pd. content "
    sql += "	WHEN 0 THEN '収録'"
    sql += "	WHEN 1 THEN '練習'"
    sql += "	WHEN 2 THEN '配信'"
    sql += "END AS content, "
    sql += "w.title, "
    sql += "pd.hour, "
    sql += "pd.money "
    sql += "FROM appMoney_payment_detail AS pd "
    sql += "INNER JOIN appMoney_payment AS p "
    sql += "ON pd.activity_id = p.id "
    sql += "LEFT OUTER JOIN appWorks_works AS w "
    sql += "ON pd.work_id = w.id "

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

    # 立替金テーブルデータ取得
    data = Payment_detail.objects.raw(sql)
    
    # ページネーション設定
    page = Paginator(data, 5)

    # 列名
    col = ('日付', '場所', '活動内容', '作品', '時間', '金額')  

    params= {
        'title':'さらぼー管理/立替金詳細',
        'type':'立替金詳細',
        'msg':message,
        'inputForm':paymentDetailForm(),
        'searchForm':searchPaymentDetailForm(),
        'data':page.get_page(num),
        'col':col,
        'sumPos':'',
        'chk':chk,
    }

    if 'input' in request.POST:
        params['inputForm'] = paymentDetailForm(request.POST)

        # 登録ラジオボタンにチェック
        params['chk'] = False

    elif 'search' in request.POST:
        params['searchForm'] = searchPaymentDetailForm(request.POST)

        # 検索ラジオボタンにチェック
        params['chk'] = True

    return render(request, 'appMoney/blance.html', params)



# 編集ページ表示
@login_required
def edit(request, page, id):

    # 変数初期化
    info_message = 'ID:' + str(id) + 'のデータを編集します'
    type = ''

    # ページごとにテーブルを変更
    if page == 'blance':
        obj = Pos.objects.get(id = id)
        type = '残高'
        sent_form = posModelForm(instance=obj)

    elif page == 'payment':
        obj = Payment.objects.get(id = id)
        type = '立替金'
        sent_form = paymentModelForm(instance=obj)

    else:
        obj = Payment_detail.objects.get(id = id)
        type = '立替金詳細'
        sent_form = detailModelForm(instance=obj)

    # POST送信判定
    if request.method == 'POST':
        # ページごとに処理変更
        if page == 'blance':
            editData = posModelForm(request.POST, instance=obj)
            editData.save()

        elif page == 'payment':
            editData = paymentModelForm(request.POST, instance=obj)
            editData.save()

        else:
            editData = detailModelForm(request.POST, instance=obj)
            editData.save()

        # メッセージを設定
        global message
        message = 'データを更新しました。'

        # リダイレクト
        return redirect(to='/appMoney/' + page)

    params = {
            'title':type + '更新',
            'info':info_message,
            'form':sent_form,
        }

    return render(request, 'appMoney/edit.html', params)


# 削除ページ表示
@login_required
def delete(request, page, id):
        
    # 変数初期化
    info_message = 'ID:' + str(id) + 'のデータを削除します'
    type = ''

    # ページごとにテーブルを変更
    if page == 'blance':
        obj = Pos.objects.get(id = id)
        type = '残高'

    elif page == 'payment':
        obj = Payment.objects.get(id = id)
        type = '立替金'

    else:
        obj = Payment_detail.objects.get(id = id)
        type = '立替金詳細'

    # POST送信判定
    if request.method == 'POST':
        # データを削除
        obj.delete()

        # メッセージを設定
        global message
        message = 'データを削除しました。'

        # リダイレクト
        return redirect(to='/appMoney/' + page)

    params = {
            'title':type + '削除',
            'type':type,
            'info':info_message,
            'obj':obj,
        }

    return render(request, 'appMoney/delete.html', params)


# 作品ごと集計ページ表示
@login_required
def works_sum(request, num=1):

    # リスト初期化
    havingSQL = []

    # 変数初期化
    workID = ''
    radio = '0'

    # POST送信判定
    if (request.method == 'POST'):
        # 検索処理(having句)
        havingSQL = search(request, 3)

        # 作品検索
        workID = request.POST['works']

        # 配信検索
        if request.POST['radio'] == '0':
            # 未選択は検索しない
            radio = ''
        else:
            radio = '0'

    # データ抽出SQL作成
    sql =  "SELECT w.id, "
    sql += "w.title, "
    sql += "SUM(pd.hour) AS hourSum, "
    sql += "SUM(pd.money) AS moneySum "
    sql += "FROM appMoney_payment_detail AS pd "
    sql += "INNER JOIN appWorks_works AS w "
    sql += "ON pd.work_id = w.id "

    if workID != '':
        # workIDがある場合は検索する
        sql += "WHERE w.id = '" + workID + "' "

    sql += "GROUP BY w.id, w.title "

    if havingSQL:
        # 条件を追加
        sql += ' HAVING '

        # ループをカウント
        i = 0

        for SQL in havingSQL:
            if i == 0:
                # ループ一回目
                sql += SQL
            else:
                # ループ二回目以降
                sql += 'AND ' + SQL

            # カウントアップ
            i += 1

    if radio == '0':
        # 0ならラジオも検索する
        sql += " UNION "
        sql += "SELECT 0 AS id, "
        sql += "'配信' AS title, "
        sql += "SUM(pd.hour) AS hourSum, "
        sql += "SUM(pd.money) AS moneySum "
        sql += "FROM appMoney_payment_detail AS pd "
        sql += "WHERE pd.content = 2 "
        sql += "GROUP BY pd.content "

        if havingSQL:
            # 条件を追加
            sql += ' HAVING '

            # ループをカウント
            i = 0

            for SQL in havingSQL:
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

    # 立替金テーブルデータ取得
    data = Payment_detail.objects.raw(sql)
    
    # ページネーション設定
    page = Paginator(data, 5)

    params= {
        'title':'さらぼー管理/作品ごと集計',
        'type':'作品ごと集計',
        'msg':message,
        'searchForm':worksSumForm(),
        'data':page.get_page(num),
    }

    if 'search' in request.POST:
        params['searchForm'] = worksSumForm(request.POST)

    return render(request, 'appMoney/works_sum.html', params)


# 画面処理以外の関数
''' 登録データ作成
    引数: request
          mode  0:残高テーブル更新
                1:立替金テーブル更新
                2:立替金詳細テーブル更新
    戻り値 登録データ(辞書)
'''
def create(request, mode):

    global message
    global money_1hour

    if mode == 0:
        # 残高テーブル登録データ
        chkDate = request.POST['posDate']     # 日付

        # 日付チェック
        posDate = checkDate(chkDate)

        # 日付不正の場合処理を抜ける
        if posDate == '':
            message = "日付が不正のため、登録できませんでした。"

            return False

        blance = request.POST['blance']       # 収支

        # ユーザー
        user = getUser(request)

        money = request.POST['money']         # 金額

        # 備考
        if request.POST['note'] == '':
            # 未記入はnull
            note = None
        else:
            note = request.POST['note']           

        # 立替金No
        if request.POST['paymentNo'] == 0:
            # 0はなし
            paymentNo = None
        else:
            paymentNo = request.POST['paymentNo']

        # 辞書に格納
        data = {'posDate':posDate, 
                'blance':blance, 
                'user':user, 
                'money':money, 
                'note':note,
                'paymentNo':paymentNo}

    elif mode == 1:
        # 立替金テーブル登録データ
        chkDate = request.POST['payDate']   # 日付

        # 日付チェック
        payDate = checkDate(chkDate)

        # 日付不正の場合処理を抜ける
        if payDate == '':
            message = "日付が不正のため、登録できませんでした。"

            return False

        place = request.POST['place']   # 場所
        
        # ユーザー
        user = getUser(request)

        hour = request.POST['hour']         # 時間
        money = request.POST['money']       # 金額

        # 精算チェック
        if ('payoff' in request.POST):
            # チェックありはTrue
            payoff = True
        else:
            # チェックなしはFalse
            payoff = False

        money_1hour = float(money) / float(hour)    # 1時間あたりの金額

        # 辞書に格納
        data = {'payDate':payDate, 
                'place':place, 
                'user':user, 
                'hour':hour,
                'money':money, 
                'money_1hour':round(money_1hour),
                'payoff':payoff}

    else:
        # 立替金詳細データ
        activity_id = request.POST['activity_id']   # 立替金ID
        content = request.POST['content']           # 活動内容
        
        # 作品ID
        if request.POST['works'] == '':
            # 未選択はNULL
            work_id = None
        else:
            work_id = request.POST['works'] 
            
        hour = request.POST['hour']                 # 時間

        # 金額算出
        money = calcMoney(activity_id, hour)

        # 辞書に格納
        data = {'activity_id':activity_id, 
                'content':content, 
                'work_id':work_id, 
                'hour':hour,
                'money':money, 
                }

    # 辞書を返す
    return data

''' データの検索
    引数: request
          mode  0:残高テーブル検索
                1:立替金テーブル検索
                2:立替金詳細テーブル検索
                3:作品ごと集計検索(ここで作るのは数値のみ)
    戻り値 WHERE句SQL(リスト)
'''
def search(request, mode): 
    # 戻り値の初期化
    ans = []

    # 変数初期化
    table = ""

    if mode == 0:
        # 残高テーブル検索       
        # 文字列検索対象
        noteWhere = request.POST['choiceNoteStr']      # 備考検索条件

        # 辞書に格納{検索項目：検索条件(0:完全一致、1:前方一致、2:後方一致)}
        strData = {
                'note':noteWhere,
            }

        # 数値検索対象
        moneyWhere = request.POST['choiceMoneyInt']    # 金額検索条件

        # 辞書に格納{検索項目：検索条件(0:一致、1:以上、2:以下)}
        intData = {
                'money':moneyWhere,
            }

        # その他検索対象
        posDate = request.POST['posDate']   # 日付

        # 収支検索
        if request.POST['blance'] == '2':
            # 2は検索しない
            blance = ''
        else:
            blance = request.POST['blance']

        # 立替金検索
        if request.POST['paymentNo'] == '0':
            # 0は検索しない
            paymentNo = ''
        else:
            paymentNo = request.POST['paymentNo']

        # ユーザー検索
        user = getUser(request)

        # 辞書に格納{検索項目：検索値}
        eachData = {
                'posDate':posDate,
                'blance':blance,
                'paymentNo':paymentNo,
                'user':user,
                }

    elif mode == 1:
        # 立替金テーブル検索
        # 文字列はないのでダミー
        strData = {}
        
        # 数値検索対象
        hourWhere = request.POST['choiceHourInt']      # 時間検索条件
        moneyWhere = request.POST['choiceMoneyInt']    # 金額検索条件

        # 辞書に格納{検索項目：検索条件(0:一致、1:以上、2:以下)}
        intData = {
                    'hour':hourWhere,
                    'money':moneyWhere,
            }

        # その他検索対象
        payDate = request.POST['payDate']   # 日付

        # 収支検索
        if request.POST['place'] == '2':
            # 2は検索しない
            place = ''
        else:
            place = request.POST['place']

        # 精算チェック検索
        if request.POST['payoff'] == '2':
            # 0は検索しない
            payoff = ''
        else:
            payoff = request.POST['payoff']

        # ユーザー検索
        user = getUser(request)

        # 辞書に格納{検索項目：検索値}
        eachData = {
                'payDate':payDate,
                'place':place,
                'payoff':payoff,
                'user':user,
                }

    elif mode == 2:
        # 詳細テーブル検索
        table = "pd."
        
        # 文字列はないのでダミー
        strData = {}

        # 数値検索対象
        hourWhere = request.POST['choiceHourInt']      # 時間検索条件
        moneyWhere = request.POST['choiceMoneyInt']    # 金額検索条件

        # 辞書に格納{検索項目：検索条件(0:一致、1:以上、2:以下)}
        intData = {
                    'hour':hourWhere,
                    'money':moneyWhere,
            }

        # その他検索対象
        activity_id = request.POST['activity_id']   # 立替金ID
        
        # 活動内容
        if request.POST['content'] == '3':
            # 3は検索しない
            content = ''
        else:
            content = request.POST['content']

        # 作品
        title = getWork(request)

        # 辞書に格納{検索項目：検索値}
        eachData = {
                'pd.activity_id':activity_id,
                'pd.content':content,
                'w.title':title,
                }

    else:
        # 作品ごと集計検索
        # 文字列はないのでダミー
        strData = {}

        # 数値検索対象
        hourWhere = request.POST['choiceHourInt']      # 時間検索条件
        moneyWhere = request.POST['choiceMoneyInt']    # 金額検索条件

        # 辞書に格納{検索項目：検索条件(0:一致、1:以上、2:以下)}
        intData = {
                    'hourSum':hourWhere,
                    'moneySum':moneyWhere,
            }

        # その他はないのでダミー
        eachData = {}

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

''' 残高を算出
    引数: なし
    戻り値 算出した残高
'''
def calcPos():
    
    # 収入データを取得
    income = Pos.objects.filter(blance=0).aggregate(Sum('money'))

    # 支出データを取得
    expense = Pos.objects.filter(blance=1).aggregate(Sum('money'))

    # 残高を算出(収入 - 支出)
    sumPos = int(income['money__sum']) - int(expense['money__sum'])

    return sumPos

''' ユーザー名を取得
    引数: request
    戻り値 ユーザー名
           未選択の場合、空文字を返す
'''
def getUser(request):
    
    if request.POST['user'] == '':
        # 空の場合処理を終了
        return ''

    # ユーザーID
    userID = request.POST['user'] 
        
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

''' 活動内容ごとの金額を算出
    引数: id      立替金ID
          hour    時間
    戻り値 算出した金額
'''
def calcMoney(id, hour):
    # 1時間あたりの金額取得(オブジェクト)
    getObj = Payment.objects.values('money_1hour').get(id=id)

    # オブジェクトから金額取得
    money = getObj['money_1hour']

    # 金額を計算
    ans = float(money) * float(hour)

    return ans