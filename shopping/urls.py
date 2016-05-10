from django.conf.urls import url
from django.contrib import admin

from .views import ( product_detail,
                     products_list,
                     product_create_from_category,
                     categories_list,
                     category_create,
                     order_list,
                     order_detail,
                     order_create,
                     order_actual,
                     order_pdf,
                     customer_create,
                     customer_list,
                     customer_detail,
                     index,
                     help_view,
)

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^categories/$', categories_list, name='categories_list'),
    url(r'^categories/create/$', category_create, name='category_create'),
    url(r'^categories/(?P<id>\d+)/$', products_list, name='products_list'),
    url(r'^categories/(?P<id>\d+)/create', product_create_from_category, name='product_create_from_category'),
    url(r'^categories/(?P<id_category>\d+)/(?P<id_product>\d+)/$', product_detail, name='product_detail'),
    url(r'^orders/$', order_list, name='order_list'),
    url(r'^orders/create/$', order_create, name='order_create'),
    url(r'^orders/actual/$', order_actual, name='order_actual'),
    url(r'^orders/(?P<id>\d+)/$', order_detail, name='order_detail'),
    url(r'^orders/(?P<id>\d+)/pdf/$', order_pdf, name='order_pdf'),
    url(r'^customers/$', customer_list, name='customer_list'),
    url(r'^customers/(?P<id>\d+)/$', customer_detail, name='customer_detail'),
    url(r'^customers/create/$', customer_create, name='customer_create'),
    url(r'^help/$', help_view, name='help_view'),
]
