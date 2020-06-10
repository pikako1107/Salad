from django.db import models

# Create your models here.
class Works(models.Model):
    # 作品テーブル
    title = models.TextField(max_length=200)
    writer = models.TextField(max_length=45)
    editor = models.TextField(max_length=45)
    illustrator = models.TextField(max_length=45)
    animator = models.TextField(max_length=45)
    completion_date = models.DateField()
