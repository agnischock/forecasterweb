from django.db import models
import datetime

# Create your models here.
from django.db import models
from django.utils import timezone


class Upd(models.Model):
    # product_id | integer | nÒo nulo
    # channel_id | integer | nÒ nulo
    # manual | boolean |
    # upper_limit | numeric(15, 2) |
    # lower_limit | numeric(15, 2) |
    # forecast | boolean |
    # cv | numeric |
    # incidence_rate
    product_id = models.IntegerField(null=False)
    channel_id = models.IntegerField(null=False)
    manual = models.BooleanField()
    upper_limit = models.FloatField()
    lower_limit = models.FloatField()
    forecast = models.BooleanField()
    cv = models.FloatField()
    incidence_rate = models.FloatField()

class UpdDetails(models.Model):
    # id | integer | nÒo
    # product_id | integer | nÒo
    # channel_id | integer | nÒo
    # date | date | nÒo
    # quantity | numeric(10, 3) | nÒo
    # outlier | boolean | nÒo
    # manual

    product_id = models.IntegerField(null=False)
    channel_id = models.IntegerField(null=False)
    date = models.DateTimeField('forecast date')
    quantity = models.IntegerField(default=0)
    outlier = models.BooleanField()
    manual = models.BooleanField()

# class Forecast(models.Model):
#     def __str__(self):
#         # Here it would be interesting to get the math model name, but it would be needed to access the math_models table
#         forecast_name = str(self.product_id) + '-' + str(self.channel_id) + '-' + str(self.math_model_id)
#         return forecast_name
#
#     def was_published_recently(self):
#         return self.date >= timezone.now() - datetime.timedelta(days=365)
#
#     def forecast_identifier():
#         forecast_id = self.product_id + '-' + self.channel_id + '-' + self.math_model_id
#         return forecast_id
#
#     math_model_id = models.IntegerField(null=False)
#     product_id = models.IntegerField(null=False)
#     channel_id = models.IntegerField(null=False)
#     mse = models.FloatField(null=True)
#     utheil = models.FloatField(null=True)
#     bias = models.FloatField(null=True)
#     date = models.DateTimeField('date published')
#     version = models.IntegerField()
#     status = models.IntegerField()
#     alpha = models.FloatField(null=True)
#     beta = models.FloatField(null=True)
#     gamma = models.FloatField(null=True)
#     r_squared = models.FloatField(null=False, default=0)
#
# class ForecastDetails(models.Model):
#     class Meta:
#         # managed = False
#         db_table = 'forecasts_details'
#     def __str__(self):
#         return self.forecast_id
#
#     forecast_id = models.ForeignKey(Forecast, on_delete=models.CASCADE)
#     date = models.DateTimeField('forecast date')
#     quantity = models.IntegerField(default=0)

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
