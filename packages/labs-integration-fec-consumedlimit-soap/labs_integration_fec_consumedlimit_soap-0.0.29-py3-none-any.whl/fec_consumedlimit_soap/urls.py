# Django Imports
from django.conf.urls import url, include
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoView
from fec_consumedlimit_soap.views import FECConsumedLimitService

# Project Imports
# from fec_consumedlimit_soap.views import GetDetails

# urlpatterns = [
#     url(r'^get-details/$', GetDetails.as_view(), name='get-details')
# ]

urlpatterns = [
    url(r'^limit/', DjangoView.as_view(
        services=[
            FECConsumedLimitService], tns='fec_consumedlimit_soap.views',
        in_protocol=Soap11(validator='lxml'), out_protocol=Soap11(),
        cache_wsdl=False)),
]
