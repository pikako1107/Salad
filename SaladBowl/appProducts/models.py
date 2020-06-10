from django.db import models

# Create your models here.
class Products(models.Model):
    id = models.IntegerField(primary_key=True)
    set_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=45)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.IntegerField()
    owner = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'

class SetProducts(models.Model):
    set_id = models.IntegerField(primary_key=True)
    set_name = models.CharField(max_length=45)
    price = models.DecimalField(max_digits=10, decimal_places=0)

    class Meta:
        managed = False
        db_table = 'set_products'

    def __str__(self):
        return self.set_name

class Sales(models.Model):
    sales_id = models.IntegerField(primary_key=True)
    date = models.DateField()
    type = models.IntegerField()
    type_id = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=0)
    count = models.IntegerField()
    other = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'sales'