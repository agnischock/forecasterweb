from django.urls import include, path

from . import views

app_name = 'forecaster'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:product_id>-<int:channel_id>/', views.detail, name='detail'),
    path('run/', views.model_parametrization, name='parametrization'),
    # path('gchartsdetail/<int:product_id>-<int:channel_id>/', views.detailg, name='gchartsdetail'),
    path('gchartsdetail/<int:product_id>-<int:channel_id>/', views.ForecastsDetailsGcharts.as_view(), name='gchartsdetail'),
    # path('upds/channel_branch', views.ChannelBranches.as_view(), name='load_channel_branch'),
    path('upds/product_branch', views.ProductBranches.as_view(), name='load_product_branch'),
    path('upds/channel_branch', views.ChannelBranches.as_view(), name='load_channel_branch')

]