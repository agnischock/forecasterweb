# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class ForecasterForecast(models.Model):
    math_model_id = models.IntegerField()
    product_id = models.IntegerField()
    channel_id = models.IntegerField()
    mse = models.FloatField(blank=True, null=True)
    utheil = models.FloatField(blank=True, null=True)
    bias = models.FloatField(blank=True, null=True)
    date = models.DateTimeField()
    version = models.IntegerField()
    status = models.IntegerField()
    alpha = models.FloatField(blank=True, null=True)
    beta = models.FloatField(blank=True, null=True)
    gamma = models.FloatField(blank=True, null=True)
    r_squared = models.FloatField()

    class Meta:
        managed = False
        db_table = 'forecaster_forecast'


class ForecasterForecastdetails(models.Model):
    date = models.DateTimeField()
    quantity = models.IntegerField()
    forecast_id = models.ForeignKey(ForecasterForecast, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'forecaster_forecastdetails'


class ForecasterUpd(models.Model):
    product_id = models.IntegerField()
    channel_id = models.IntegerField()
    manual = models.BooleanField()
    upper_limit = models.FloatField()
    lower_limit = models.FloatField()
    forecast = models.BooleanField()
    cv = models.FloatField()
    incidence_rate = models.FloatField()

    class Meta:
        managed = False
        db_table = 'forecaster_upd'


class ForecasterUpddetails(models.Model):
    product_id = models.IntegerField()
    channel_id = models.IntegerField()
    date = models.DateTimeField()
    quantity = models.IntegerField()
    outlier = models.BooleanField()
    manual = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'forecaster_upddetails'


class Forecasts(models.Model):
    math_model_id = models.IntegerField()
    product = models.ForeignKey('Upds', models.DO_NOTHING)
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


class PollsChoice(models.Model):
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField()
    question = models.ForeignKey('PollsQuestion', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'polls_choice'


class PollsQuestion(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'polls_question'


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
