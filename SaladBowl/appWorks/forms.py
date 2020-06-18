from django import forms
from .models import Works, Cast, Progress
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

# 作品登録フォーム
class worksForm(forms.Form):
    # タイトル
    title = forms.CharField(label="作品名", 
                           max_length=200) 
    # 脚本
    writer = forms.ModelChoiceField(queryset=User.objects.all(),
                                    label="脚本", 
                                    to_field_name="id") 
    # 編集
    editor = forms.ModelChoiceField(queryset=User.objects.all(),
                                    label="編集", 
                                    to_field_name="id") 
    # イラスト
    illustrator = forms.ModelChoiceField(queryset=User.objects.all(),
                                    label="イラスト", 
                                    to_field_name="id") 
    # 動画
    animator = forms.ModelChoiceField(queryset=User.objects.all(),
                                    label="動画", 
                                    to_field_name="id") 
    # 完了チェック
    completion = forms.BooleanField(label="完了チェック", required=False)

# 作品検索フォーム
class searchWorksForm(forms.Form):
    # タイトル(ID)
    title = forms.ModelChoiceField(queryset=Works.objects.all(),
                                    label="作品", 
                                    to_field_name="id",
                                    required=False)

    # 脚本
    writer = forms.ModelChoiceField(queryset=User.objects.all(),
                                    label="脚本", 
                                    to_field_name="id",
                                    required=False) 
    # 編集
    editor = forms.ModelChoiceField(queryset=User.objects.all(),
                                    label="編集", 
                                    to_field_name="id",
                                    required=False) 
    # イラスト
    illustrator = forms.ModelChoiceField(queryset=User.objects.all(),
                                    label="イラスト", 
                                    to_field_name="id",
                                    required=False) 
    # 動画
    animator = forms.ModelChoiceField(queryset=User.objects.all(),
                                    label="動画", 
                                    to_field_name="id",
                                    required=False) 

    # 検索用完了チェック
    listCompletion = [
            (0, '未完'),
            (1, '完了'),
            (2, '未選択')
        ]

    # 完了チェック
    completion = forms.ChoiceField(label="完了チェック", 
                               choices=listCompletion,
                               required=False,
                               initial=[2, '未選択'])

# キャスト登録フォーム
class castForm(forms.Form):
    # タイトルID
    workID = forms.ModelChoiceField(queryset=Works.objects.all(),
                                    label="作品", 
                                    to_field_name="id")
    # キャラクター
    character = forms.CharField(label="キャラクター", 
                                max_length=45)
    # ユーザー取得
    user = User.objects.all()

    # リストを初期化
    listCast = [
            (-1, 'ゲスト'),
            (-2, '未定')
        ]

    # リストにデータ追加
    for item in user:
        listCast.append((item.id, item.name))
    
    # キャスト
    cast = forms.ChoiceField(choices=listCast,
                            label="キャスト") 
    # ステータス
    status = forms.BooleanField(label="ステータス", required=False)

# キャスト検索フォーム
class searchCastForm(forms.Form):
    # タイトルID
    workID = forms.ModelChoiceField(queryset=Works.objects.all(),
                                    label="作品", 
                                    to_field_name="id",
                                    required=False)
    # キャラクター
    character = forms.CharField(label="キャラクター", 
                                max_length=45,
                                required=False)

    # キャラクター検索項目
    choiceChara = forms.ChoiceField(label="キャラクター検索条件",
                                   choices=nameRadioData,
                                   required=False,
                                   initial=[0, '完全一致'],
                                   widget=forms.RadioSelect())  

    # ユーザー取得
    user = User.objects.all()

    # リストを初期化
    listCast = [
            (-1, 'ゲスト'),
            (-2, '未定'),
            (-3, '未選択')
        ]

    # リストにデータ追加
    for item in user:
        listCast.append((item.id, item.name))
    
    # キャスト
    cast = forms.ChoiceField(choices=listCast,
                            label="キャスト", 
                            required=False,
                            initial=[-3, '未選択']) 
    # 検索用ステータス
    listStatus = [
            (0, '収録中'),
            (1, '完了'),
            (2, '未選択')
        ]

    # 完了チェック
    status = forms.ChoiceField(label="ステータス", 
                               choices=listStatus,
                               required=False,
                               initial=[2, '未選択'])

# 進捗検索フォーム
class searchProgressForm(forms.Form):
    # タイトルID
    workID = forms.ModelChoiceField(queryset=Works.objects.all(),
                                    label="作品", 
                                    to_field_name="id",
                                    required=False)
    # 収録進捗
    castPro = forms.IntegerField(label="収録進捗", 
                               required=False)
    # 収録進捗検索項目
    choiceCastPro = forms.ChoiceField(label="収録進捗検索条件",
                                    choices=intRadioData,
                                    required=False,
                                    initial=[0, '一致'],
                                    widget=forms.RadioSelect()) 
    # 編集担当
    editor = forms.ModelChoiceField(queryset=User.objects.all(),
                                    label="編集担当", 
                                    to_field_name="id",
                                    required=False) 
    # 検索用進捗
    listProgress = [
            (0, '作業中'),
            (1, '完了'),
            (2, '未選択')
        ]

    # 編集進捗
    editPro = forms.ChoiceField(label="編集進捗", 
                               choices=listProgress,
                               required=False,
                               initial=[2, '未選択'])

    # イラスト担当
    illustrator = forms.ModelChoiceField(queryset=User.objects.all(),
                                        label="イラスト担当", 
                                        to_field_name="id",
                                        required=False) 
    # イラスト進捗
    illustPro = forms.ChoiceField(label="イラスト進捗", 
                                   choices=listProgress,
                                   required=False,
                                   initial=[2, '未選択'])
    # 動画担当
    animator = forms.ModelChoiceField(queryset=User.objects.all(),
                                label="動画担当", 
                                to_field_name="id",
                                required=False) 
    # 動画進捗
    animaPro = forms.ChoiceField(label="動画進捗", 
                                choices=listProgress,
                                required=False,
                                initial=[2, '未選択'])
    # 進捗率
    allPro = forms.IntegerField(label="進捗率", 
                               required=False)

    # 進捗率検索項目
    choiceAllPro = forms.ChoiceField(label="進捗率検索条件",
                                    choices=intRadioData,
                                    required=False,
                                    initial=[0, '一致'],
                                    widget=forms.RadioSelect()) 

# 作品モデルフォーム
class worksModelForm(forms.ModelForm):
    class Meta:
        model = Works
        fields = ['title', 'writer', 'editor', 'illustrator', 'animator', 'completion']

# キャストモデルフォーム
class castModelForm(forms.ModelForm):
    class Meta:
        model = Cast
        fields = ['workID', 'character', 'cast', 'status']

# 進捗モデルフォーム
class progressModelForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = ['workID', 'editPro', 'illustPro', 'animaPro']


