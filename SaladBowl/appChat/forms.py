from django import forms
from . import models
from appChat.models import Room

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