from django.db import models

# Create your models here.
class User(models.Model):
    # ユーザーテーブル
    name = models.TextField(max_length=45)

    def __str__(self):
        return self.name