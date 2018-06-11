from .models import Upds, UpdsDetails, Forecasts, ForecastsDetails, MathModels

class ColplanRouter(object):

    def db_for_read(self, model, **hints):
        """ reading SomeModel from otherdb """
        model_list = [Upds, UpdsDetails, ForecastsDetails, Forecasts, MathModels]
        if model in model_list:
            return 'colplan'
        return None

    def db_for_write(self, model, **hints):
        """ writing SomeModel to otherdb """
        model_list = [Upds, UpdsDetails, ForecastsDetails, Forecasts, MathModels]
        if model in model_list:
            return 'colplan'
        return None
