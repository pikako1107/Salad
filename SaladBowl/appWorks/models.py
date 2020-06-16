from django.db import models

# Create your models here.
class Works(models.Model):
    # 作品テーブル
    title = models.CharField(max_length=200)
    writer = models.CharField(max_length=45)
    editor = models.CharField(max_length=45)
    illustrator = models.CharField(max_length=45)
    animator = models.CharField(max_length=45)
    completion = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Cast(models.Model):
    # キャストテーブル
    workID = models.IntegerField()
    character = models.CharField(max_length=45)
    cast = models.CharField(max_length=45)
    status = models.BooleanField(default=False)

class Progress(models.Model):
    # 進捗テーブル
    workID = models.IntegerField()
    editPro = models.BooleanField(default=False)
    illustPro = models.BooleanField(default=False)
    animaPro = models.BooleanField(default=False)
