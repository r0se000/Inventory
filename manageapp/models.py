from django.db import models

# Create your models here.
class Input(models.Model):
    device = models.ForeignKey('Product', primary_key=True, on_delete=models.CASCADE)
    input_date = models.DateField()
    price = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'input'


class Output(models.Model):
    device = models.ForeignKey('Product', primary_key=True, on_delete=models.CASCADE)
    output_date = models.DateField()
    cus_name = models.CharField(max_length=15)

    class Meta:
        #managed = False
        db_table = 'output'


class Product(models.Model):
    device_id = models.CharField(primary_key=True, max_length=8)
    p_name = models.CharField(max_length=8)

    class Meta:
        #managed = False
        db_table = 'product'