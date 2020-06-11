from django import forms
from . import models
from .models import Pos, Payment, Payment_detail
from appManagement.models import User

# グローバル変数
nameRadioData = [
        (0, '完全一致'),
        (1, '前方一致'),
        (2, '後方一致')
    ]                       # 名称検索項目

intRadioData = [
        (0, '一致'),
        (1, '以上'),
        (2, '以下')
    ]                       # 数値検索項目

listBlance = [
        (0, '収入'),
        (1, '支出'),
    ]                       # 収支リスト

# 収支登録フォーム
class posForm(forms.Form): 
    
    posDate = forms.DateField(label="日付")  # 日付

    # 収支選択
    blance = forms.ChoiceField(label="収支", 
                                choices=listBlance, 
                                initial=[0, '収入'],
                                widget=forms.RadioSelect())

    # ユーザー名
    human = forms.ModelChoiceField(queryset=User.objects.all(),
                                    label="ユーザー", 
                                    to_field_name="id")     

    money = forms.IntegerField(label="金額")                # 金額
    note = forms.CharField(label="備考", 
                           max_length=200,
                           required=False)                  # 備考

    # 立替金情報抽出SQL作成
    sql = 'SELECT id, payDate, place '
    sql += 'FROM appMoney_payment;'

    # 立替金情報取得
    payment = Payment.objects.raw(sql)

    # リストを初期化
    listPayment = [(0, 'なし')]

    # 立替金情報をタプルに格納
    for item in payment:

        if item.place == 0:
            strPlace = '会議室'
        else:
            strPlace = 'スタジオ'

        listPayment.append((item.id, str(item.payDate) + '：' + strPlace))

    # 立替金
    paymentNo = forms.ChoiceField(label="立替金", 
                                    choices=listPayment,
                                    initial=[0, 'なし'],
                                    required=False)     # 立替金No


# 収支検索フォーム
class searchPosForm(forms.Form):

    posDate = forms.DateField(label="日付", 
                           required=False)  # 日付

    # 収支リストに追加
    listBlance.append((2, '両方'))

    # 収支選択
    blance = forms.ChoiceField(label="収支", 
                                choices=listBlance, 
                                initial=[2, '両方'],
                                required=False,
                                widget=forms.RadioSelect())
        
    # ユーザー名
    human = forms.ModelChoiceField(queryset=User.objects.all(),
                                    label="ユーザー", 
                                    to_field_name="id",
                                    required=False)   

    money = forms.IntegerField(label="金額", required=False)     # 金額

    choiceMoneyInt = forms.ChoiceField(label="金額検索条件",
                                    choices=intRadioData,
                                    required=False,
                                    initial=[0, '一致'],
                                    widget=forms.RadioSelect())  # 金額検索項目

    note = forms.CharField(label="備考", 
                           max_length=200,
                           required=False)                       # 備考

    choiceNoteStr = forms.ChoiceField(label="備考検索条件",
                                    choices=nameRadioData,
                                    required=False,
                                    initial=[0, '完全一致'],
                                    widget=forms.RadioSelect())  # 備考検索項目

    # 立替金情報抽出SQL作成
    sql = 'SELECT id, payDate, place '
    sql += 'FROM appMoney_payment;'

    # 立替金情報取得
    payment = Payment.objects.raw(sql)

    # リストを初期化
    listPayment = [(0,'未選択')]

    # 立替金情報をタプルに格納
    for item in payment:

        if item.place == 0:
            strPlace = '会議室'
        else:
            strPlace = 'スタジオ'

        listPayment.append((item.id, str(item.payDate) + '：' + strPlace))

    # 立替金
    paymentNo = forms.ChoiceField(label="立替金", 
                                    choices=listPayment,
                                    initial=[0, '未選択'],
                                    required=False)     # 立替金No

