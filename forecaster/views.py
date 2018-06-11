from django.shortcuts import render, reverse

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.http import Http404
from django.template import loader
from django.core.paginator import Paginator
from django.views import View
from django.db.models import Sum
from django.db import connection, connections

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

import matplotlib

matplotlib.use('Agg')
from matplotlib import pyplot as plt
import mpld3
# from mpld3 import plugins
from suds.client import Client
import pylab
import json

from .models import Forecasts, ForecastsDetails, Upds, UpdsDetails, MathModels
from .forms import BranchForm


# Create your views here.



def get_level(product_or_channel):
    with connections['colplan'].cursor() as cursor:
        query = """	SELECT "c"."value" FROM "configs" AS "c" WHERE "c"."name" = 'upd_%s_level'"""
        query = query % product_or_channel
        cursor.execute(query)
        level = int(cursor.fetchone()[0])

    return level

def get_parent_level(product_or_channel, id):
    with connections['colplan'].cursor() as cursor:
        query = """	SELECT level FROM {0} AS "t" WHERE "t"."id" = '{1}'"""
        table = product_or_channel + 's'
        query = query.format(table, id)
        cursor.execute(query)
        level = int(cursor.fetchone()[0])

    return level

def index(request):
    # forecast_list = Forecast.objects.order_by('product_id','channel_id')[:5]
    # template = loader.get_template('polls/index.html')
    upd_list = Forecasts.objects.all().order_by('product_id', 'channel_id').distinct('product_id', 'channel_id')
    form_products = BranchForm(identifier='products', level=get_level('product'))
    form_channels = BranchForm(identifier='channels', level=get_level('channel'))
    print(get_level('channel'))
    print(get_level('product'))

    print(form_products.branch_items)
    context = {'upd_list': upd_list, 'form_products':form_products, "form_channels":form_channels }
    # return HttpResponse(template.render(context, request))
    return render(request, 'forecaster/index.html', context)


def detail(request, product_id, channel_id):

    p_id = product_id
    c_id = channel_id
    values = []
    dates = []
    upd = str(p_id) + '-' + str(c_id)

    upd_list = Forecasts.objects.all().order_by('product_id', 'channel_id').distinct('product_id', 'channel_id')
    paginator = Paginator(upd_list, 1)
    #
    page = request.GET.get('page', 1)
    # upds = paginator.get_page(page)

    try:
        upds = paginator.page(page)
    except PageNotAnInteger:
        upds = paginator.page(1)
    except EmptyPage:
        upds = paginator.page(paginator.num_pages)

    math_models_objects = MathModels.objects.all()
    print(math_models_objects)
    math_models = {}
    for mm in math_models_objects:
        math_models[mm.id] = mm.description

    upd_details = UpdsDetails.objects.order_by('date').filter(product_id=p_id, channel_id=c_id)
    for detail in upd_details:
        values.append(detail.quantity)
        dates.append(detail.date)

    # fig = plt.figure()
    fig, ax = plt.subplots()
    ax.grid(True, alpha=0.3)

    l, = ax.plot(dates, values, label='Faturamento')
    legends = ['Datas', 'Faturamento']
    model_time_series_list = []
    model_time_series_list.append(values)

    model_list = Forecasts.objects.order_by('math_model_id').filter(product_id=p_id, channel_id=c_id)
    least_theil = Forecasts.objects.order_by('utheil').filter(product_id=p_id, channel_id=c_id)[1]
    min_theil_name = math_models[least_theil.math_model_id]

    for model in model_list:
        forecast_id = model.id
        forecast_math_model_id = model.math_model_id
        theil = model.utheil

        forecast_list = ForecastsDetails.objects.order_by('date').filter(forecast_id=forecast_id)

        values = []
        dates = []
        for forecast in forecast_list:
            values.append(float(forecast.quantity))
            dates.append(forecast.date)
        model_time_series_list.append(values)
        # plt.plot(dates, values, 'ks-', mec='w', mew=5, ms=20)
        # l, = ax.plot(dates, values, label=str(forecast_math_model))
        l, = ax.plot(dates, values, label=math_models[forecast_math_model_id] + '-' + str(theil))
        legends.append(math_models[forecast_math_model_id])
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
    # context = {'upd': upd, 'div_figure' : g, 'min_theil' : min_theil_name, 'upds' : upds}
    graph_data = [dates]
    for i in model_time_series_list:
        graph_data.append(i)
    print(graph_data)
    graph_data = [list(i) for i in zip(*graph_data)]
    print(graph_data)
    data = [legends]
    for i in graph_data:
        data.append(i)
    print(data)

    # context = {'upd': upd, 'div_figure' : g, 'min_theil' : min_theil_name, 'data': data}


    context = {'upd': upd, 'div_figure': g, 'min_theil': min_theil_name}

    return render(request, 'forecaster/detail.html', context)


def model_parametrization(request):
    context = {}
    print(request.POST)
    # If no parameter was checked, returns None
    parameters = dict(request.POST).get('parametro')
    print(parameters)
    horizon = dict(request.POST).get('horizon')
    upd_years = dict(request.POST).get('time_series_size_years')

    if parameters == None:
        return render(request, 'forecaster/parametrization.html', context)
    else:
        print('ok')

        rmoutlier = False
        suav = False
        season = False
        trend = False
        amort = False
        preseason = False

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
            if p == 'reseason':
                preseason = True

        ## Invoke add method of MetodosService
        wsdl_url = 'http://localhost:8085/MetodosService?wsdl'
        client = Client(url=wsdl_url, cache=None, timeout=300)
        if preseason:
            print(client.service.calcular(empresaId='ae2b6e0c-ca46-4887-a253-5ceba10e3721', removerOutlier=rmoutlier,
                                          suavizarDados=suav, ligarSazonalidade=season, tendencia=trend,
                                          amortizar=amort,
                                          reseason=preseason, horizon=horizon, data_size=upd_years))
        else:
            print(client.service.calcular(empresaId='ae2b6e0c-ca46-4887-a253-5ceba10e3721', removerOutlier=rmoutlier,
                                          suavizarDados=suav, ligarSazonalidade=season, tendencia=trend,
                                          amortizar=amort, horizon=horizon, data_size=upd_years))

        print("Response received")
        print(client)

        return HttpResponseRedirect(reverse('forecaster:index'))


class ForecasterDetails(View):
    def forecast_data(self, product_id, channel_id):
        p_id = product_id
        c_id = channel_id
        values = []
        dates = []

        upd_details = UpdsDetails.objects.order_by('date').filter(product_id=p_id, channel_id=c_id)
        for detail in upd_details:
            values.append(float(detail.quantity))
            dates.append(str(detail.date))

        forecasts_details_data = {}
        forecasts_details_data['Faturamento'] = dict(zip(dates, values))

        model_list = Forecasts.objects.order_by('math_model_id').filter(product_id=p_id, channel_id=c_id)
        math_models_objects = MathModels.objects.all()
        math_models = {}
        for mm in math_models_objects:
            math_models[mm.id] = mm.description

        for model in model_list:
            forecast_id = model.id
            forecast_math_model_id = model.math_model_id
            forecast_list = ForecastsDetails.objects.order_by('date').filter(forecast_id=forecast_id)

            values = []
            dates = []
            for forecast in forecast_list:
                values.append(float(forecast.quantity))
                dates.append(str(forecast.date))
            forecasts_details_data[str(math_models[forecast_math_model_id])] = dict(zip(dates, values))

        return forecasts_details_data


class ForecastsDetailsGcharts(ForecasterDetails):
    def get(self, request, product_id, channel_id):
        context = super(ForecastsDetailsGcharts, self).forecast_data(product_id, channel_id)

        return JsonResponse(context)

class ForecastsDetailsAggregatedGcharts(View):
    def get(self, request, product_id, channel_id):
        product_level = get_parent_level('product', product_id)
        channel_level = get_parent_level('channel', channel_id)
        product_level_max = get_level('product')
        channel_level_max = get_level('channel')

        sql_string = """
            select 	
                "ud".date,
                sum("ud".quantity) 
            from upds_details as "ud" 
            join (select distinct on (c{5}_id, c{1}_id) c{5}_id max_c, c{1}_id agg_c from view_channels_tree where c{1}_id='4') as "vc" on "vc".max_c="ud".channel_id 
            join  (select distinct on (p{4}_id, p{0}_id) p{4}_id max_p, p{0}_id agg_p from view_products_tree where p{0}_id='8') as "vp" on "vp".max_p="ud".product_id
            group by 
                "vp".agg_p,
                "vc".agg_c, 
                "ud".date 
            order by 
                "vp".agg_p,
                "vc".agg_c, 
                "ud".date;
        """
        # {0} = product_level
        # {1} = channel_level
        # {2} = product_id
        # {3} = channel_id
        # {4} = product_level_max 3
        # {5} = channel_level_max 2

        # product_level = 2
        # channel_level = 2
        # product_id = '13'
        # channel_id = '4'
        # product_level_max = 3
        # channel_level_max = 2
        sql_string= sql_string.format(product_level, channel_level, product_id, channel_id, product_level_max, channel_level_max)
        print(sql_string)

        with connections['colplan'].cursor() as cursor:
            cursor.execute(sql_string)

            branch_items = cursor.fetchall()
            print(branch_items)
        # return HttpResponse(template.render(context, request))
        dates = []
        values = []
        for item in branch_items:
            dates.append(str(item[0]))
            values.append(item[1])
        upd_aggregate = dict(zip(dates, values))
        context = {'Faturamento': upd_aggregate,}

        return JsonResponse(context)


class Branches(View):
    """ Branch loading base class, generic for product or chanel """

    parent_id = ""
    identifier = ""

    def sql_branch(self):
        query = "select id as id,description as description from %s where parent_id=%s;"
        print(self.identifier)
        print(self.parent_id)

        query = query % (self.identifier, self.parent_id)
        print(query)
        return query

    def load_branch(self):

        with connections['colplan'].cursor() as cursor:
            query = self.sql_branch()
            cursor.execute(query)

            branch_items = cursor.fetchall()
            print(branch_items)
        # return HttpResponse(template.render(context, request))
        return branch_items

    def get(self, request):

        branch_items = self.load_branch()
        branch_dicts = []
        for item in branch_items:
            branch_dicts.append({'id': item[0], 'description': item[1]})

        # form = BranchForm()
        context = {'branch_items': branch_dicts}

        return render(request, 'forecaster/tree_dropdown_list_options.html', context)
    
class ChannelBranches(Branches):

    identifier = "channels"

    def get(self, request):
        channel_id = request.GET.get('channel_id')
        self.parent_id = channel_id

        return super(ChannelBranches, self).get(request)

class ProductBranches(Branches):

    identifier = "products"

    def get(self, request):
        product_id = request.GET.get('product_id')
        self.parent_id = product_id

        return super(ProductBranches, self).get(request)

        


