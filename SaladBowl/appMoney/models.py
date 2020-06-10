from django.db import models

# Create your models here.
class Pos(models.Model):
    # 残高テーブル
    date = models.DateField()
    blance = models.IntegerField()
    human = models.TextField(max_length=45)
    money = models.DecimalField(max_digits=10, decimal_places=0)
    note = models.TextField(max_length=200, blank=True, null=True)
    paymentNo = models.IntegerField(blank=True, null=True)


class Payment(models.Model):
    # 立替金テーブル
    date = models.DateField()
    place = models.IntegerField()
    human = models.TextField(max_length=45)
    money = models.DecimalField(max_digits=10, decimal_places=0)
    hour = models.IntegerField()
    money_1hour = models.IntegerField()
    payoff = models.BooleanField()


class Payment_detail(models.Model):
    # 立替金_詳細テーブル
    activity_id = models.IntegerField()
    place = models.IntegerField()
    content = models.IntegerField()
    hour = models.IntegerField()
    money = models.DecimalField(max_digits=10, decimal_places=0)

