from django.urls import include, path

from . import views

app_name = 'forecaster'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:product_id>-<int:channel_id>/', views.detail, name='detail'),
]