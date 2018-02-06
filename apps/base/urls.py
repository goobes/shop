"""urlconf for the base application"""

from django.conf.urls import url

from .views import home, check_profile, make_payment, payment_redirect, payment_webhook
from .views import ProfileCreate, ProfileDetail, ItemList, ItemDetail


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^profile/check/$', check_profile, name='profile-check'),
    url(r'^profile/create/$', ProfileCreate.as_view(), name='profile-create'),
    url(r'^profile/(?P<pk>[^/]+)$', ProfileDetail.as_view(), name='profile-detail'),
    url(r'^payment/create/(?P<pk>[^/]+)$', make_payment, name='payment-create'),
    url(r'^payment/redirect/(?P<pk>[^/]+)$', payment_redirect, name='payment-redirect'),
    url(r'^payment/webhook/$', payment_webhook, name='payment-webhook'),
    url(r'^shop/$', ItemList.as_view(), name='shop'),
    url(r'^shop/(?P<pk>[^/]+)$', ItemDetail.as_view(), name='shop-item')
]
