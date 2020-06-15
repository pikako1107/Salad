from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import productsForm, setsForm, salesForm, productsModelForm, setsModelForm, salesModelForm, productsSearchForm, setsSearchForm, salesSearchForm
from .models import Products, SetProducts, Sales
from django.db.models import Max
from django.shortcuts import redirect
from . import forms
import datetime

# Create your views here.
# グローバル変数
message = ''

# (True:検索、False:登録)
chk = True

# 在庫ページ表示
@login_required
def products(request, num=1):

    global chk

    # リスト初期化
    whereSQL = []

    # POST送信判定
    if (request.method == 'POST'):

        # ボタン判定
        if 'input' in request.POST:
            # 登録処理
            # IDの最大値を取得
            maxID = Products.objects.aggregate(Max('id'))

            # 登録するIDを取得(最大値+1)
            insertID = maxID['id__max'] + 1

            # 登録関数呼び出し
            dictData = create(request, 0)

            # インスタンス作成
            insertData = Products(id = insertID,
                                  set_id = dictData['セットID'],
                                  name = dictData['商品名'],
                                  price = dictData['値段'],
                                  stock = dictData['在庫'],
                                  owner = dictData['所持者'])

            # 保存
            insertData.save()

            global message
            message = "データを登録しました。"

        else:
            # 検索処理
            whereSQL = search(request, 0)

    # SQL
    sql = 'SELECT p.id, p.name, p.price, s.set_name, p.stock, p.owner '
    sql += 'FROM products AS p '
    sql += 'LEFT OUTER JOIN set_products AS s '
    sql += 'ON p.set_id = s.set_id'

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

    # productsテーブルのデータを取得
    data = Products.objects.raw(sql)

    # ページネーション設定
    page = Paginator(data, 5)

    # 列名
    col = ('ID', '商品名', '値段', 'セット', '在庫', '所持者')
    
    params= {
            'title':'さらぼー管理/在庫',
            'type':'在庫',
            'msg':message,
            'inputForm':productsForm(),
            'searchForm':productsSearchForm(),
            'col':col,
            'data':page.get_page(num),
            'chk':chk,
        }

    if 'input' in request.POST:
        params['inputForm'] = productsForm(request.POST)
        
        # 登録ラジオボタンにチェック
        params['chk'] = False

    elif 'search' in request.POST:
        params['searchForm'] = productsSearchForm(request.POST)

        # 検索ラジオボタンにチェック
        params['chk'] = True

    return render(request, 'appProducts/products.html', params)

# セットページ表示
@login_required
def sets(request, num=1):

    global chk

    # リスト初期化
    whereSQL = []

    # POST送信判定
    if (request.method == 'POST'):

        # ボタン判定
        if 'input' in request.POST:
            # IDの最大値を取得
            maxID = SetProducts.objects.aggregate(Max('set_id'))

            # 登録するIDを取得(最大値+1)
            insertID = maxID['set_id__max'] + 1

            # 登録関数呼び出し
            dictData = create(request, 1)

            # インスタンス作成
            insertData = SetProducts(set_id = insertID,
                                     set_name = dictData['セット名'],
                                     price = dictData['値段'])

            # 保存
            insertData.save()

            global message
            message = "データを登録しました。"

        else:  
            # 検索処理
            whereSQL = search(request, 1)

            sql = "SELECT * FROM set_products "

    # データ取得
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

        sql += ';'
        data = SetProducts.objects.raw(sql)

    else:
        data = SetProducts.objects.all()

    # ページネーション設定
    page = Paginator(data, 5)

    # 列名
    col = ('ID', 'セット名', '値段')

    params= {
            'title':'さらぼー管理/セット',
            'type':'セット',
            'msg':message,
            'inputForm':setsForm(),
            'searchForm':setsSearchForm(),
            'col':col,
            'data':page.get_page(num),
            'chk':chk,
        }

    if 'input' in request.POST:
        params['inputForm'] = setsForm(request.POST)
        
        # 登録ラジオボタンにチェック
        params['chk'] = False

    elif 'search' in request.POST:
        params['searchForm'] = setsSearchForm(request.POST)

        # 検索ラジオボタンにチェック
        params['chk'] = True

    return render(request, 'appProducts/products.html', params)

# 売上ページ表示
@login_required
def sales(request, num=1):

    global chk

    # リスト初期化
    whereSQL = []

    # POST送信判定
    if (request.method == 'POST'):

        # ボタン判定
        if 'input' in request.POST:
            # IDの最大値を取得
            maxID = Sales.objects.aggregate(Max('sales_id'))

            # 登録するIDを取得(最大値+1)
            insertID = maxID['sales_id__max'] + 1

            # 登録関数呼び出し
            dictData = create(request, 2)

            # falseが戻ってきたら処理を抜ける
            if dictData != False:
                # インスタンス作成
                insertData = Sales(sales_id = insertID,
                                   date = dictData['日付'],
                                   type = dictData['売上種別'],
                                   type_id = dictData['売上商品ID'],
                                   price = dictData['単価'],
                                   count = dictData['売上個数'],
                                   other = dictData['特記事項'])

                # 保存
                insertData.save()

                # ダウンロード販売は除く
                if dictData['特記事項'] != 'ダウンロード販売':
                    # 在庫から売り上げた個数を引く
                    stockCount(int(dictData['売上種別']), 
                               int(dictData['売上商品ID']), 
                               int(dictData['売上個数']))

                global message
                message = "データを登録しました。"

        else:
            # 検索処理
            whereSQL = search(request, 2)

    # 売上データ取得SQL
    sql = 'SELECT s.sales_id, s.date, s.type, p.name, s.price, s.count, s.other '
    sql += 'FROM sales AS s '
    sql += 'INNER JOIN products AS p '
    sql += 'ON s.type_id = p.id '
    sql += 'WHERE s.type = 0 '

    if whereSQL:
        for SQL in whereSQL:
            sql += 'AND ' + SQL

    sql += 'UNION '
    sql += 'SELECT s.sales_id, s.date, s.type, p.set_name, s.price, s.count, s.other '
    sql += 'FROM sales AS s '
    sql += 'INNER JOIN set_products AS p '
    sql += 'ON s.type_id = p.set_id '
    sql += 'WHERE s.type = 1 '
    
    if whereSQL:
        for SQL in whereSQL:
            sql += 'AND ' + SQL

    sql += 'ORDER BY sales_id;'

    # データ取得
    data = Sales.objects.raw(sql)

    # ページネーション設定
    page = Paginator(data, 5)

    # 列名
    col = ('ID', '日付', '売上種別','商品/セット名','単価','売上個数','特記事項')

    params= {
            'title':'さらぼー管理/売上',
            'type':'売上',
            'msg':message,
            'inputForm':salesForm(),
            'searchForm':salesSearchForm(),
            'col':col,
            'data':page.get_page(num),
            'chk':chk,
        }

    if 'input' in request.POST:
        params['inputForm'] = salesForm(request.POST)
        
        # 登録ラジオボタンにチェック
        params['chk'] = False

    elif 'search' in request.POST:
        params['searchForm'] = salesSearchForm(request.POST)

        # 検索ラジオボタンにチェック
        params['chk'] = True

    return render(request, 'appProducts/products.html', params)

# 編集ページ表示
@login_required
def edit(request, page, id):

    # 変数初期化
    info_message = 'ID:' + str(id) + 'のデータを編集します'
    type = ''

    # ページごとにテーブルを変更
    if page == 'products':
        obj = Products.objects.get(id = id)
        type = '在庫'
        sent_form = productsModelForm(instance=obj)

    elif page == 'sets':
        obj = SetProducts.objects.get(set_id = id)
        type = 'セット'
        sent_form = setsModelForm(instance=obj)

    else:
        obj = Sales.objects.get(sales_id = id)
        type = '売上'
        sent_form = salesModelForm(instance=obj)

    # POST送信判定
    if request.method == 'POST':
        # ページごとに処理変更
        if page == 'products':
            editData = productsModelForm(request.POST, instance=obj)
            editData.save()

        elif page == 'sets':
            editData = setsModelForm(request.POST, instance=obj)
            editData.save()

        else:
            editData = salesModelForm(request.POST, instance=obj)
            editData.save()

        # メッセージを設定
        global message
        message = 'データを更新しました。'

        # リダイレクト
        return redirect(to='/appProducts/' + page)

    params = {
            'title':type + '更新',
            'info':info_message,
            'form':sent_form,
        }

    return render(request, 'appProducts/edit.html', params)

# 削除ページ表示
@login_required
def delete(request, page, id):
        
    # 変数初期化
    info_message = 'ID:' + str(id) + 'のデータを削除します'
    type = ''

    # ページごとにテーブルを変更
    if page == 'products':
        obj = Products.objects.get(id = id)
        type = '在庫'

    elif page == 'sets':
        obj = SetProducts.objects.get(set_id = id)
        type = 'セット'

    else:
        obj = Sales.objects.get(sales_id = id)
        type = '売上'

    # POST送信判定
    if request.method == 'POST':
        # データを削除
        obj.delete()

        # メッセージを設定
        global message
        message = 'データを削除しました。'

        # リダイレクト
        return redirect(to='/appProducts/' + page)

    params = {
            'title':type + '削除',
            'type':type,
            'info':info_message,
            'obj':obj,
        }

    return render(request, 'appProducts/delete.html', params)


# 画面処理以外の関数

''' 登録データ作成
    引数: request
          mode  0:商品テーブル更新
                1:セットテーブル更新
                2:売上テーブル更新  
    戻り値 登録データ(辞書)
'''
def create(request, mode):

    if mode == 0:
        # 商品テーブルデータ取得
        name = request.POST['name']     # 商品名
        price = request.POST['price']   # 値段
        set_id = request.POST['set_id'] 

        # セットID
        if request.POST['set_id'] == '':
            set_id = None
        else:
            set_id = request.POST['set_id']

        stock = request.POST['stock']   # 在庫
        owner = request.POST['owner']   # 所持者

        # 辞書に格納
        data = {'商品名':name, 
                '値段':price, 
                'セットID':set_id, 
                '在庫':stock, 
                '所持者':owner}

    elif mode == 1:
        # セットテーブルデータ取得
        set_name = request.POST['set_name'] # セット名
        price = request.POST['price']       # 値段

        # 辞書に格納
        data = {'セット名':set_name,
                '値段':price}

    else:
        # 売上テーブルデータ取得
        # 日付
        chkDate = request.POST['date']                 
        
        # 日付チェック
        date = checkDate(chkDate)

        # 日付不正の場合処理を抜ける
        if date == '':
            global message
            message = "日付が不正のため、登録できませんでした。"

            return False

        sale_choice = request.POST['sale_choice']   # 売上種別
        name_id = request.POST['name']              # 売上商品のID
        price = request.POST['price']               # 値段
        count = request.POST['count']               # 売上個数

        # 特記事項
        if request.POST['other'] == '0':
            other = None
        else:
            other = 'ダウンロード販売'

        # 辞書に格納
        data = {'日付':date,
                '売上種別':sale_choice,
                '売上商品ID':name_id,
                '単価':price,
                '売上個数':count,
                '特記事項':other}

    # 辞書を返す
    return data


''' 在庫から売上個数を引く
    引数: type      売上種別
                    0:個別　1:セット
          type_id   売上商品のID  
          count     売上個数
    戻り値 なし
'''
def stockCount(type, type_id, count):

    if type == 0:
        # 個別
        updateData = Products.objects.get(id=type_id)
        # 在庫 - 売上個数
        updateData.stock = updateData.stock - count
        # データ更新
        updateData.save()

    else:
        # セット
        updateData = Products.objects.filter(set_id=type_id)

        # 在庫 - 売上個数
        for list in updateData:
            list.stock = list.stock - count
            # データ更新
            list.save()


''' データの検索
    引数: request
          mode  0:商品テーブル検索
                1:セットテーブル検索
                2:売上テーブル検索
    戻り値 WHERE句SQL(リスト)
'''
def search(request, mode): 
    # 戻り値の初期化
    ans = []

    # 変数初期化
    table = ""

    # 処理わけ
    if mode == 0:
        # メイン取得テーブル
        table = "p."

        # 文字列検索対象
        nameWhere = request.POST['choiceName']      # 商品名検索条件
        ownerWhere = request.POST['choiceOwner']    # 所持者検索条件

        # 辞書に格納{検索項目：検索条件(0:完全一致、1:前方一致、2:後方一致)}
        strData = {
                'name':nameWhere,
                'owner':ownerWhere,
            }

        # 数値検索対象
        priceWhere = request.POST['choicePrice']    # 値段検索条件
        stockWhere = request.POST['choiceStock']    # 在庫検索条件

        # 辞書に格納{検索項目：検索条件(0:一致、1:以上、2:以下)}
        intData = {
                'price':priceWhere,
                'stock':stockWhere,
            }

        # その他検索対象
        set_id = request.POST['set_id'] # セットID検索値

        # 辞書に格納{検索項目：検索値}
        eachData = {
                's.set_id':set_id,
                }

    elif mode == 1:
        # セットテーブル
        # 文字列検索対象
        nameWhere = request.POST['choiceName']      # セット名検索条件

        # 辞書に格納{検索項目：検索条件(0:完全一致、1:前方一致、2:後方一致)}
        strData = {
                'set_name':nameWhere,
            }

        # 数値検索対象
        priceWhere = request.POST['choicePrice']    # 値段検索条件

        # 辞書に格納{検索項目：検索条件(0:一致、1:以上、2:以下)}
        intData = {
                'price':priceWhere,
            }

        # その他はないのでダミー
        eachData = {}

    else:
        # 売上テーブル
        table = "s."

        # 文字列はないのでダミー
        strData = {}

        # 数値検索対象
        priceWhere = request.POST['choicePrice']    # 値段検索条件
        countWhere = request.POST['choiceCount']    # 個数検索条件

        # 辞書に格納{検索項目：検索条件(0:一致、1:以上、2:以下)}
        intData = {
                'price':priceWhere,
                'count':countWhere,
            }

        # その他検索対象
        date = request.POST['date']                     # 日付検索値
        
        if request.POST['sale_choice'] == '2':
            # 2は検索しない
            sale_choice = ''
        else:
            sale_choice = request.POST['sale_choice']   # 売上種別検索値

        if request.POST['name'] == '0':
            # 0は検索しない
            nameID = ''
        else:
            nameID = request.POST['name']               # 商品ID

        if request.POST['choiceOther'] == '0':          # 特記事項
            # 0は検索しない
            other = ''
        else:
            other = 'ダウンロード販売'

        # 辞書に格納{検索項目：検索値}
        eachData = {
                's.date':date,
                's.type':sale_choice,
                's.type_id':nameID,
                's.other':other,
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

