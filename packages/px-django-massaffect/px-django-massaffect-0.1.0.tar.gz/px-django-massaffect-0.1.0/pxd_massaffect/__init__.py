__version__ = '0.1.0'

from django.utils.module_loading import autodiscover_modules


VERSION = tuple(__version__.split('.'))

default_app_config = 'pxd_massaffect.apps.SalesConfig'


def autodiscover():
    autodiscover_modules('sales')
