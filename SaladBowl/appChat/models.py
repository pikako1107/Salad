from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
class Room(models.Model):
    # ルームテーブル
    name = models.CharField(max_length=200) # ルーム名

    def __str__(self):
        return self.name

class Chat(models.Model):
    # チャットテーブル
    roomID = models.IntegerField()                  # ルームID
    user = models.CharField(max_length=45)          # ユーザー名
    posttime = models.DateTimeField()               # 登校時間
    comment = models.CharField(max_length=1000)     # コメント

class File(models.Model):
    # ファイルテーブル
    name = models.CharField(max_length=200)                 # ファイル名
    uptime = models.DateTimeField()                         # アップロード日時
    roomID = models.IntegerField()                          # ルームID
    deadlineDate = models.DateField()                       # 確認期限

    uploadplace = models.FileField(validators=[FileExtensionValidator(['mp3','wav','ogg', ])],)     # 保存場所

class Check(models.Model):
    # 確認状況テーブル
    fileID = models.IntegerField()                  # ファイルID
    roomID = models.IntegerField()                  # ルームID
    user = models.CharField(max_length=45)          # ユーザー名
    check = models.BooleanField(default=False)      # 確認状況  true:確認済み　false:未確認
    checkdate = models.DateField(blank=True, 
                                 null=True)         # 確認日   null:未確認　日付:確認済み

