from django.conf import settings
from appconf import AppConf

class FECAppIDConf(AppConf):
    END_POINT = settings.WORKFLOW_BASE_URL + '/enquiry/gcl/'
    END_POINT = settings.WORKFLOW_BASE_URL_FOR_CONSUMED_LIMIT + '/enquiry/gcl/'
    END_POINT_WL = settings.WORKFLOW_BASE_URL_FOR_CONSUMED_LIMIT_WL + '/enquiry/gcl/'


    class Meta:
        prefix = 'cons'