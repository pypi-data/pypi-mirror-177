from datetime import datetime

from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from fec_consumedlimit_soap.models import FECConsumedLimit
from spyne.application import Application
from spyne.const.xml_ns import DEFAULT_NS
from spyne.decorator import rpc
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.service import ServiceBase
from spyne.util.django import DjangoComplexModel
from fec_consumedlimit_soap.service import ConsumedService, ConsumedServiceWl
from fec_consumedlimit_soap.utils import update_consumed_limit_from_lms_views


class ConsumedLimitRequestContainer(DjangoComplexModel):
    class Attributes(DjangoComplexModel.Attributes):
        django_model = FECConsumedLimit
        django_exclude = [
            'NumberOfApplications',
            'TotalConsumedLimit',
            'TotalEMI',
            'created_at',
            'updated_at'
        ]


class ConsumedLimitResponseContainer(DjangoComplexModel):
    class Attributes(DjangoComplexModel.Attributes):
        django_model = FECConsumedLimit
        django_exclude = [
            'PersonId',
            'NationalID',
            'FromDate',
            'ToDate',
            'created_at',
            'updated_at'
        ]


class FECConsumedLimitService(ServiceBase):
    """
    This handles both create and get APIs for Consumed Limit.
    """

    __namespace__ = DEFAULT_NS

    @rpc(ConsumedLimitRequestContainer, _returns=ConsumedLimitResponseContainer)
    def get_limit(ctx, container):
        try:
            if not container.NationalID:
                raise ValidationError('ListPersonIds and ListNationalIds are missing.')
            if not container.PersonId:
                container.PersonId = ''

            consumedlimit_service_obj = ConsumedService(request=None, request_id=None,
                                                           nationalIds=container.NationalID,
                                                           personIds=container.PersonId,
                                                           cache_flag=None, callback_url=None)
            c_limit_object = consumedlimit_service_obj.call_api()
            consumedlimit_service_obj_2 = ConsumedServiceWl(request=None, request_id=None,
                                                           nationalIds=container.NationalID,
                                                           personIds=container.PersonId,
                                                           cache_flag=None, callback_url=None)
            c_limit_object_2 = consumedlimit_service_obj_2.call_api()
            if c_limit_object:
                adjusted_limit,count  = update_consumed_limit_from_lms_views(container.NationalID, c_limit_object)
                c_limit_object['TotalConsumedLimit'] = adjusted_limit
                c_limit_object['NumberOfApplications'] = count
            else:
                c_limit_object['TotalConsumedLimit'] = 0
                c_limit_object['NumberOfApplications'] = 0

            if c_limit_object_2:
                adjusted_limit,count  = update_consumed_limit_from_lms_views(container.NationalID, c_limit_object_2)
                c_limit_object_2['TotalConsumedLimit'] = adjusted_limit
                c_limit_object_2['NumberOfApplications'] = count
            else:
                c_limit_object_2['TotalConsumedLimit'] = 0
                c_limit_object_2['NumberOfApplications'] = 0
            c_limit_object['TotalConsumedLimit'] = c_limit_object['TotalConsumedLimit'] + c_limit_object_2['TotalConsumedLimit']
            c_limit_object['NumberOfApplications'] = c_limit_object['NumberOfApplications'] + c_limit_object_2['NumberOfApplications']
            return c_limit_object

        except (FECConsumedLimit.DoesNotExist, ValidationError) as e:
            return FECConsumedLimit()

app = Application([FECConsumedLimitService],
                  'fec_consumedlimit_soap.views',
                  in_protocol=Soap11(validator='lxml'),
                  out_protocol=Soap11(),
                  )

hello_world_service = csrf_exempt(DjangoApplication(app))
