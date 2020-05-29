from django import forms
from . import models
from django.contrib.auth import forms as auth_forms
from .models import Products, SetProducts, Sales

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

# ログインフォーム
class LoginForm(auth_forms.AuthenticationForm):
    '''ログインフォーム'''
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

# 商品フォーム
class productsForm(forms.Form):
    
    name = forms.CharField(label="商品名", max_length=45)     # 商品名
    price = forms.IntegerField(label="値段")                  # 値段
    set_id = forms.ModelChoiceField(queryset=models.SetProducts.objects.all(),
                                    label="セット", 
                                    to_field_name="set_id",
                                    required=False)           # セット
    stock = forms.IntegerField(label="在庫")                  # 在庫
    owner = forms.CharField(label="所持者", 
                            max_length=45,
                            required=False)                   # 所持者


# セットフォーム
class setsForm(forms.Form):

    set_name = forms.CharField(label="セット名", max_length=45)     # 商品名
    price = forms.IntegerField(label="値段")                        # 値段

# 売上フォーム
class salesForm(forms.Form):

    date = forms.DateField(label="日付")      # 売上日付
    
    # 売上種別
    sale_type = [
            (0, "個別"),
            (1, "セット")
        ]

    sale_choice = forms.ChoiceField(label="売上種別", choices=sale_type, widget=forms.RadioSelect())
    
    # SQL
    sql =   "SELECT id, name "
    sql +=  "FROM products "
    sql +=  "UNION "
    sql +=  "SELECT set_id, set_name "
    sql +=  "FROM set_products;"

    # 売上商品
    sale_products = Products.objects.raw(sql)

    # リストを初期化
    list_products = []

    # 売上商品をタプルに格納
    for item in sale_products:
        list_products.append((item.id, item.name))

    
    # 売上商品
    name = forms.ChoiceField(label="売上商品", choices=list_products)

    price = forms.IntegerField(label="単価")                          # 単価
    count = forms.IntegerField(label="売上個数")                      # 売上個数


# 商品モデルフォーム
class productsModelForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = ['set_id', 'name', 'price', 'stock', 'owner']

# セットモデルフォーム
class setsModelForm(forms.ModelForm):
    class Meta:
        model = SetProducts
        fields = ['set_name', 'price']

# 売上モデルフォーム
class salesModelForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['date', 'type', 'type_id', 'price', 'count']


# 在庫検索フォーム
class productsSearchForm(forms.Form):

    name = forms.CharField(label="商品名", 
                           max_length=45, 
                           required=False)                      # 商品名

    choiceName = forms.ChoiceField(label="商品検索条件",
                                   choices=nameRadioData,
                                   required=False,
                                   initial=[0, '完全一致'],
                                   widget=forms.RadioSelect())  # 商品検索項目

    price = forms.IntegerField(label="値段", 
                               required=False)                  # 値段

    choicePrice = forms.ChoiceField(label="値段検索条件",
                                    choices=intRadioData,
                                    required=False,
                                    initial=[0, '一致'],
                                    widget=forms.RadioSelect()) # 値段検索項目

    set_id = forms.ModelChoiceField(queryset=models.SetProducts.objects.all(),
                                    label="セット", 
                                    to_field_name="set_id",
                                    required=False)             # セット

    stock = forms.IntegerField(label="在庫", 
                               required=False)                  # 在庫

    choiceStock = forms.ChoiceField(label="在庫検索条件",
                                    choices=intRadioData,
                                    required=False,
                                    initial=[0, '一致'],
                                    widget=forms.RadioSelect()) # 在庫検索項目

    owner = forms.CharField(label="所持者", 
                            max_length=45,
                            required=False)                     # 所持者

    choiceOwner = forms.ChoiceField(label="所持者検索条件",
                                    choices=nameRadioData,
                                    required=False,
                                    initial=[0, '完全一致'],
                                    widget=forms.RadioSelect()) # 所持者検索項目