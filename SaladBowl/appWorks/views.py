from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Works, Cast, Progress
from .forms import worksForm, searchWorksForm

# グローバル変数
message = ''

# (True:検索、False:登録)
chk = True

# Create your views here.
# 作品ページ表示
@login_required
def works(request, num=1):
    # POST送信判定
    if (request.method == 'POST'):
        pass

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
    sql += "        END AS completion "
    sql += "FROM "
    sql += "        appWorks_works "

    # 末尾にセミコロン追加
    sql += ';'

    # 残高テーブルデータ取得
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
def cast(request):
    pass

# 進捗ページ表示
@login_required
def progress(request):
    pass

# 作業集計ページ表示
@login_required
def work_count(request):
    pass