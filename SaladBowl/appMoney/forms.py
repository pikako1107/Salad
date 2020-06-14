from django import forms
from . import models
from .models import Pos, Payment, Payment_detail
from appManagement.models import User
from appWorks.models import Works

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

listPlace = [
        (0, '会議室'),
        (1, 'スタジオ')
    ]                       # 場所リスト

listContents = [
        (0, '収録'),
        (1, '練習'),
        (2, '配信')
    ]                       # 活動内容リスト

# 収支登録フォーム
class posForm(forms.Form): 
    
    posDate = forms.DateField(label="日付")  # 日付

    # 収支選択
    blance = forms.ChoiceField(label="収支", 
                                choices=listBlance, 
                                initial=[0, '収入'],
                                widget=forms.RadioSelect())

    # ユーザー名
    user = forms.ModelChoiceField(queryset=User.objects.all(),
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

# 立替金登録フォーム
class paymentForm(forms.Form):
    
    # 日付
    payDate = forms.DateField(label="日付")           
    
    # 場所
    place = forms.ChoiceField(label="場所", 
                            choices=listPlace,
                            initial=[0, '会議室'])    

    # ユーザー
    user = forms.ModelChoiceField(queryset=User.objects.all(),
                                    label="ユーザー", 
                                    to_field_name="id")  
    # 時間
    hour = forms.FloatField(label="時間")                

    # 金額
    money = forms.IntegerField(label="金額")     
    
    # 精算チェック
    payoff = forms.BooleanField(label="精算チェック", required=False)


# 立替金検索フォーム
class searchPaymentForm(forms.Form):
    # 日付
    payDate = forms.DateField(label="日付", required=False)           
    
    # 場所リストに追加
    listPlace.append((2, '未選択'))

    # 場所
    place = forms.ChoiceField(label="場所", 
                            choices=listPlace,
                            initial=[2, '未選択'],
                            required=False)    

    # ユーザー
    user = forms.ModelChoiceField(queryset=User.objects.all(),
                                    label="ユーザー", 
                                    to_field_name="id",
                                    required=False)  
    # 時間
    hour = forms.FloatField(label="時間", required=False)     
    
    choiceHourInt = forms.ChoiceField(label="時間検索条件",
                                    choices=intRadioData,
                                    required=False,
                                    initial=[0, '一致'],
                                    widget=forms.RadioSelect())  # 時間検索項目

    # 金額
    money = forms.IntegerField(label="金額", required=False)  
   
    choiceMoneyInt = forms.ChoiceField(label="金額検索条件",
                                    choices=intRadioData,
                                    required=False,
                                    initial=[0, '一致'],
                                    widget=forms.RadioSelect())  # 金額検索項目    
    
    # 検索用精算チェック
    listPayoff = [
            (0, '未済'),
            (1, '精算済み'),
            (2, '未選択')
        ]

    # 精算チェック
    payoff = forms.ChoiceField(label="精算チェック", 
                               choices=listPayoff,
                               initial=[2, '未選択'],
                               required=False)


# 立替金詳細登録フォーム
class paymentDetailForm(forms.Form):

    # 活動内容選択
    content = forms.ChoiceField(label="活動内容", 
                                choices=listContents, 
                                initial=[0, '収録'])

    # 作品選択
    works = forms.ModelChoiceField(queryset=Works.objects.all(),
                                    label="作品", 
                                    to_field_name="id",
                                    required=False)

    # 時間
    hour = forms.FloatField(label="時間")   


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
    user = forms.ModelChoiceField(queryset=User.objects.all(),
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


# 残高モデルフォーム
class posModelForm(forms.ModelForm):
    class Meta:
        model = Pos
        fields = ['posDate', 'blance', 'user', 'money', 'note', 'paymentNo']

# 立替金モデルフォーム
class paymentModelForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payDate', 'place', 'user', 'money', 'hour', 'money_1hour', 'payoff']

# 立替金詳細モデルフォーム
class detailModelForm(forms.ModelForm):
    class Meta:
        model = Payment_detail
        fields = ['content', 'work_id', 'hour', 'money']

