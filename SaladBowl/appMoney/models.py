from django.db import models

# Create your models here.
class Pos(models.Model):
    # 残高テーブル
    posDate = models.DateField()
    blance = models.IntegerField()
    user = models.CharField(max_length=45, default='')
    money = models.DecimalField(max_digits=10, decimal_places=0)
    note = models.TextField(max_length=200, blank=True, null=True)
    paymentNo = models.IntegerField(blank=True, null=True)


class Payment(models.Model):
    # 立替金テーブル
    payDate = models.DateField()
    place = models.IntegerField()
    user = models.CharField(max_length=45, default='')
    money = models.DecimalField(max_digits=10, decimal_places=0)
    hour = models.FloatField()
    money_1hour = models.IntegerField()
    payoff = models.BooleanField()

    def __str__(self):  
        if self.place == 0:
            strPlace = '会議室'
        else:
            strPlace = 'スタジオ'
        
        strDate = str(self.payDate)

        return strDate + ':' + strPlace + '(' + self.user + ')'

class Payment_detail(models.Model):
    # 立替金_詳細テーブル
    activity_id = models.IntegerField()
    content = models.IntegerField()
    work_id = models.IntegerField(blank=True, null=True)
    hour = models.FloatField()
    money = models.DecimalField(max_digits=10, decimal_places=0)

