from django import forms
from . import models
from appChat.models import Room, Chat, File

# ルーム作成フォーム
class createForm(forms.Form): 
    # ルーム名
    roomName = forms.CharField(label="ルーム名", 
                                max_length=200) 

# ルーム削除フォーム
class deleteForm(forms.Form):
    # ルーム名
    roomName = forms.ModelChoiceField(queryset=Room.objects.all(),
                                        label="ルーム名", 
                                        to_field_name="id")    

# コメント送信フォーム
class postCommentForm(forms.Form):
    # コメント入力フォーム
    comment = forms.CharField(widget=forms.Textarea(attrs={'cols': '80', 'rows': '10'}),
                              max_length=1000,
                              label="コメント")

# ファイルアップロードフォーム
class fileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('uploadplace', 'deadlineDate')
        labels = {
            'uploadplace':'ファイル選択',
            'deadlineDate':'確認期限',
            }


