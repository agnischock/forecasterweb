from django.shortcuts import render, reverse

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.template import loader

import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import mpld3
# from mpld3 import plugins
from suds.client import Client

from .models import Forecasts, ForecastsDetails

# Create your views here.

def index(request):
    # forecast_list = Forecast.objects.order_by('product_id','channel_id')[:5]
    # template = loader.get_template('polls/index.html')
    upd_list = Forecasts.objects.all().order_by('product_id', 'channel_id').distinct('product_id', 'channel_id')
    context = {'upd_list': upd_list,}
    # return HttpResponse(template.render(context, request))
    return render(request, 'forecaster/index.html', context)
def detail(request, product_id, channel_id):

    p_id = product_id
    c_id = channel_id
    values = []
    dates = []
    upd = (p_id, c_id)

    model_list = Forecasts.objects.order_by('math_model_id').filter(product_id=p_id, channel_id=c_id)

    # fig = plt.figure()
    fig, ax = plt.subplots()
    ax.grid(True, alpha=0.3)

    for model in model_list:
        forecast_id = model.id
        forecast_math_model_id = model.math_model_id
        math_models = {
            1 : 'ARRSES',
            2 : 'SES',
            3 : 'HOLT',
            4 : 'HWM',
            5 : 'HWA',
            6 : 'Decomposição Clássica',
            7 : 'Híbrido',
            8 : 'Alteração manual',
            9 : 'Previsão externa',
            10 : 'Ressazonalizado',
        }
        forecast_list = ForecastsDetails.objects.order_by('date').filter(forecast_id=forecast_id)

        values = []
        dates = []
        for forecast in forecast_list:
            values.append(forecast.quantity)
            dates.append(forecast.date)

        # plt.plot(dates, values, 'ks-', mec='w', mew=5, ms=20)
        # l, = ax.plot(dates, values, label=str(forecast_math_model))
        l, = ax.plot(dates, values, label=math_models[forecast_math_model_id])
    # plt.show()
    handles, labels = ax.get_legend_handles_labels()
    labels = ["a", "b"]
    # interactive_legend = plugins.InteractiveLegendPlugin(zip(handles,
    #                                                          ax.collections),
    #                                                      labels,
    #                                                      alpha_unsel=0.5,
    #                                                      alpha_over=1.5,
    #                                                      start_visible=True)
    # plugins.connect(fig, interactive_legend)
    ax.set_xlabel('Datas')
    ax.set_ylabel('Quantidade')
    # ax.set_title('Interactive legend', size=20)
    plt.legend()

    g = mpld3.fig_to_html(fig)
    plt.close(fig)
    context = {'upd': upd, 'div_figure' : g}

    return render(request, 'forecaster/detail.html', context)

def model_parametrization(request):
    context = {}
    print(request.POST)
    # If no parameter was checked, returns None
    parameters = dict(request.POST).get('parametro')
    print(parameters)

    # return render(request, 'forecaster/parametrization.html', context)

    if parameters==None:
        return render(request, 'forecaster/parametrization.html', context)
    else:
        print('ok')

        rmoutlier = False
        suav = False
        season = False
        trend = False
        amort = False

        for p in parameters:
            if p == 'rmoutlier':
                rmoutlier = True
            if p == 'suav':
                suav = True
            if p == 'season':
                season = True
            if p == 'trend':
                trend = True
            if p == 'amort':
                amort = True

        # import pdb;
        # pdb.set_trace()
        ## Invoke add method of MetodosService
        wsdl_url = 'http://localhost:8085/MetodosService?wsdl'
        client = Client(url=wsdl_url, cache=None, timeout=300)
        print(client.service.calcular(empresaId='ae2b6e0c-ca46-4887-a253-5ceba10e3721', removerOutlier=rmoutlier,
                                      suavizarDados=suav, ligarSazonalidade=season, tendencia=trend, amortizar=amort))

        print("Response received")
        print(client)

        return HttpResponseRedirect(reverse('forecaster:index'))
