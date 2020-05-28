from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import productsForm, setsForm, salesForm, productsModelForm, setsModelForm, salesModelForm
from .models import Products, SetProducts, Sales
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Max
from django.shortcuts import redirect
from . import forms

# Create your views here.
# ログインクラス
class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "appProducts/login.html"

# ログアウトクラス
class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "appProducts/logout.html"

# グローバル変数
message = ''

# メインページ表示
@login_required
def index(request):

    # ページURL
    goto = ('products', 'sets', 'sales')

    params = {
            'title':'さらぼー管理ツール',
            'goto':goto
        }
    return render(request, 'appProducts/index.html', params)

# 在庫ページ表示
@login_required
def products(request, num=1):

    # POST送信判定
    if (request.method == 'POST'):
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

    # SQL
    sql = 'SELECT p.id, p.name, p.price, s.set_name, p.stock, p.owner '
    sql += 'FROM products AS p '
    sql += 'LEFT OUTER JOIN set_products AS s '
    sql += 'ON p.set_id = s.set_id;'

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
            'form':productsForm(),
            'col':col,
            'data':page.get_page(num),
        }

    return render(request, 'appProducts/products.html', params)

# セットページ表示
@login_required
def sets(request, num=1):

    # POST送信判定
    if (request.method == 'POST'):
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

    # データ取得
    data = SetProducts.objects.all()

    # ページネーション設定
    page = Paginator(data, 5)

    # 列名
    col = ('ID', 'セット名', '値段')

    params= {
            'title':'さらぼー管理/セット',
            'type':'セット',
            'msg':message,
            'form':setsForm(),
            'col':col,
            'data':page.get_page(num),
        }
    return render(request, 'appProducts/products.html', params)

# 売上ページ表示
@login_required
def sales(request, num=1):

    # POST送信判定
    if (request.method == 'POST'):
        # IDの最大値を取得
        maxID = Sales.objects.aggregate(Max('sales_id'))

        # 登録するIDを取得(最大値+1)
        insertID = maxID['sales_id__max'] + 1

        # 登録関数呼び出し
        dictData = create(request, 2)

        # インスタンス作成
        insertData = Sales(sales_id = insertID,
                           date = dictData['日付'],
                           type = dictData['売上種別'],
                           type_id = dictData['売上商品ID'],
                           price = dictData['単価'],
                           count = dictData['売上個数'])

        # 保存
        insertData.save()

        # 在庫から売り上げた個数を引く
        stockCount(int(dictData['売上種別']), 
                   int(dictData['売上商品ID']), 
                   int(dictData['売上個数']))

        global message
        message = "データを登録しました。"


    # 売上データ取得SQL
    sql = 'SELECT s.sales_id, s.date, s.type, p.name, s.price, s.count '
    sql += 'FROM sales AS s '
    sql += 'INNER JOIN products AS p '
    sql += 'ON s.type_id = p.id '
    sql += 'WHERE s.type = 0 '
    sql += 'UNION '
    sql += 'SELECT s.sales_id, s.date, s.type, p.set_name, s.price, s.count '
    sql += 'FROM sales AS s '
    sql += 'INNER JOIN set_products AS p '
    sql += 'ON s.type_id = p.set_id '
    sql += 'WHERE s.type = 1 '
    sql += 'ORDER BY sales_id;'

    # データ取得
    data = Sales.objects.raw(sql)

    # ページネーション設定
    page = Paginator(data, 5)

    # 列名
    col = ('ID', '日付', '売上種別','商品/セット名','単価','売上個数')

    params= {
            'title':'さらぼー管理/売上',
            'type':'売上',
            'msg':message,
            'form':salesForm(),
            'col':col,
            'data':page.get_page(num),
        }
    return render(request, 'appProducts/products.html', params)

# 編集ページ表示
@login_required
def edit(request, page, id):

    # 変数初期化
    global message
    message = 'ID:' + str(id) + 'のデータを編集します'
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
        message = 'データを更新しました。'

        # リダイレクト
        return redirect(to='/appProducts/' + page)

    params = {
            'title':type + '更新',
            'msg':message,
            'form':sent_form,
        }

    return render(request, 'appProducts/edit.html', params)

# 削除ページ表示
@login_required
def delete(request, page, id):
        
    # 変数初期化
    global message
    message = 'ID:' + str(id) + 'のデータを削除します'
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
        message = 'データを削除しました。'

        # リダイレクト
        return redirect(to='/appProducts/' + page)

    params = {
            'title':type + '削除',
            'type':type,
            'msg':message,
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
        date = request.POST['date']                 # 日付
        sale_choice = request.POST['sale_choice']   # 売上種別
        name_id = request.POST['name']              # 売上商品のID
        price = request.POST['price']               # 値段
        count = request.POST['count']               # 売上個数

        # 辞書に格納
        data = {'日付':date,
                '売上種別':sale_choice,
                '売上商品ID':name_id,
                '単価':price,
                '売上個数':count}

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



