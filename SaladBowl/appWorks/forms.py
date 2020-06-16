from django import forms
from .models import Works, Cast, Progress
from appManagement.models import User

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
class searchWorksForm(worksForm):
    # タイトル
    title = forms.ModelChoiceField(queryset=Works.objects.all(),
                                    label="作品", 
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
    pass


