from django.db import models
import datetime

# Create your models here.
from django.db import models
from django.utils import timezone


class Forecasts(models.Model):
    math_model_id = models.IntegerField()
    product_id = models.IntegerField()
    channel_id = models.IntegerField()
    mse = models.DecimalField(max_digits=15, decimal_places=2)
    utheil = models.DecimalField(max_digits=15, decimal_places=2)
    bias = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()
    version = models.IntegerField()
    status = models.IntegerField()
    alpha = models.DecimalField(max_digits=15, decimal_places=14, blank=True, null=True)
    beta = models.DecimalField(max_digits=15, decimal_places=14, blank=True, null=True)
    gamma = models.DecimalField(max_digits=15, decimal_places=14, blank=True, null=True)
    r_squared = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'forecasts'


class ForecastsDetails(models.Model):
    forecast = models.ForeignKey(Forecasts, models.DO_NOTHING)
    date = models.DateField()
    quantity = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        managed = False
        db_table = 'forecasts_details'



class Upds(models.Model):
    product_id = models.IntegerField(primary_key=True)
    channel_id = models.IntegerField()
    manual = models.NullBooleanField()
    upper_limit = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    lower_limit = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    forecast = models.NullBooleanField()
    cv = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    incidence_rate = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'upds'
        unique_together = (('product_id', 'channel_id'),)

    def __str__(self):
        return str(self.product_id) + '-' + str(self.channel_id)


class UpdsDetails(models.Model):
    product = models.ForeignKey(Upds, models.DO_NOTHING)
    channel_id = models.IntegerField()
    date = models.DateField()
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    outlier = models.BooleanField()
    manual = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'upds_details'

    def __str__(self):
        return self.product + self.channel_id

class MathModels(models.Model):

    def __str__(self):
        return self.description

    class Meta:
        managed = False
        db_table = 'math_models'

    id = models.IntegerField(primary_key=True)
    description = models.TextField()
    manual = models.BooleanField()

