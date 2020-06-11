from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Pos, Payment, Payment_detail
from appManagement.models import User
from .forms import posForm, searchPosForm
import datetime

# Create your views here.

# グローバル変数
message = ''

# 収支管理ページ表示
@login_required
def blance(request, num=1):

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
                                human = dictData['human'],
                                money = dictData['money'],
                                note = dictData['note'],
                                paymentNo = dictData['paymentNo']
                                )

                # 保存
                insertData.save()

                global message
                message = "データを登録しました。"

        else:
            # 検索処理
            whereSQL = search(request, 0)
    
    # データ抽出SQL作成
    sql = 'SELECT id, posDate, blance, human, money, note '
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

    params= {
        'title':'さらぼー管理/収支',
        'type':'収支',
        'msg':message,
        'inputForm':posForm(),
        'searchForm':searchPosForm(),
        'data':page.get_page(num),
    }

    return render(request, 'appMoney/blance.html', params)

# 立替金登録ページ表示
@login_required
def payment_create(request):
    pass

# 立替金検索ページ表示
@login_required
def payment_search(request):
    pass

# 作品ごと集計ページ表示
@login_required
def works_sum(request):
    pass



# 画面処理以外の関数
''' 登録データ作成
    引数: request
          mode  0:残高テーブル更新
                1:立替金テーブル更新
    戻り値 登録データ(辞書)
'''
def create(request, mode):

    if mode == 0:
        # 残高テーブル登録データ
        chkDate = request.POST['posDate']     # 日付

        # 日付チェック
        posDate = checkDate(chkDate)

        # 日付不正の場合処理を抜ける
        if posDate == '':
            global message
            message = "日付が不正のため、登録できませんでした。"

            return False

        blance = request.POST['blance']       # 収支

        # ユーザーID
        userID = request.POST['human'] 
        
        getObj = User.objects.values('name').get(id=userID)
        human = getObj['name']

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
                'human':human, 
                'money':money, 
                'note':note,
                'paymentNo':paymentNo}

    else:
        # 立替金テーブル登録データ
        pass

    # 辞書を返す
    return data

''' データの検索
    引数: request
          mode  0:残高テーブル検索
                1:立替金テーブル検索
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

        # 辞書に格納{検索項目：検索値}
        eachData = {
                'posDate':posDate,
                'blance':blance,
                'paymentNo':paymentNo,
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
