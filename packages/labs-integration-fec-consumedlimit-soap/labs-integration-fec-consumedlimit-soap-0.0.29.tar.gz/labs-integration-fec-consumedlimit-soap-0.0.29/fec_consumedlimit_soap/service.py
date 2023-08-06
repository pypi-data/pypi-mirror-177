# Python Imports
import json
from datetime import datetime

# Third Party Imports
from rest_framework import status

# Project Imports
from base_app.exception_constants import NONRETRYABLE_CODE, STATUS_TYPE
from base_app.exceptions import GenericException
from base_app.serializers import ApplicationLogSerializer
from fec_consumedlimit_soap.constants import ConsConstant as cons_constants
from base_app.abstract import AbstractService
from fec_consumedlimit_soap.conf import settings


class ConsumedService(AbstractService):
    '''  '''

    def __init__(self, request, request_id, nationalIds, personIds, cache_flag=1, callback_url=None):
        # Input Parameters
        self.__nationalIds = nationalIds
        self.__personIds = personIds
        self.__cache_flag = cache_flag

        # Output Parameters
        self.__raw_result = dict()
        self.__parsed_result = dict()
        super(ConsumedService, self).__init__(
            request, request_id, callback_url, ApplicationLogSerializer)

    def make_api_input(self):
        # Defining Input Parameters
        body = {
			'listNids': self.__nationalIds,
			'listPids':  self.__personIds
		}
        # Converting Input to Json and returning to the function
        return json.dumps(body)

    def parse_response(self,response):
        data = json.loads(response)
        data['Datetime'] = datetime.now()
        data['Description'] = "Success"
        data['Code'] = '1'
        if data['status'] != 200:
            data['Description'] = "Failed"
            data['Code'] = '0'
            return data
         
        return data

    def call_api_sync(self):
        # Defining the request_url
        try:
            json_api_input = self.make_api_input()
            api_response = self.http_post_request(request_url=settings.CONS_END_POINT,
                                                  json_api_input=json_api_input,
                                                  headers=cons_constants.CONS_REQUEST_HEADER,
                                                  timeout=cons_constants.DEFAULT_HTTP_REQUEST_TIMEOUT)
            api_response_contents = api_response.content.decode('utf-8')
            if api_response.status_code == status.HTTP_200_OK:
                return self.parse_response(api_response_contents)
            else:
                return {}

        except Exception as e:
            return {}
            #raise GenericException(status_type=STATUS_TYPE["APP"], exception_code=NONRETRYABLE_CODE["BAD_REQUEST"],
            #                       detail=repr(e), request=self.request)

class ConsumedServiceWl(AbstractService):
    '''  '''

    def __init__(self, request, request_id, nationalIds, personIds, cache_flag=1, callback_url=None):
        # Input Parameters
        self.__nationalIds = nationalIds
        self.__personIds = personIds
        self.__cache_flag = cache_flag

        # Output Parameters
        self.__raw_result = dict()
        self.__parsed_result = dict()
        super(ConsumedServiceWl, self).__init__(
            request, request_id, callback_url, ApplicationLogSerializer)


    def make_api_input(self):
        # Defining Input Parameters
        body = {
			'listNids': self.__nationalIds,
			'listPids':  self.__personIds
		}
        # Converting Input to Json and returning to the function
        return json.dumps(body)

    def parse_response(self,response):
        data = json.loads(response)
        data['Datetime'] = datetime.now()
        data['Description'] = "Success"
        data['Code'] = '1'
        if data['status'] != 200:
            data['Description'] = "Failed"
            data['Code'] = '0'
            return data
         
        return data

    def call_api_sync(self):
        # Defining the request_url
        try:
            json_api_input = self.make_api_input()
            api_response = self.http_post_request(request_url=settings.CONS_END_POINT_WL,
                                                  json_api_input=json_api_input,
                                                  headers=cons_constants.CONS_REQUEST_HEADER,
                                                  timeout=cons_constants.DEFAULT_HTTP_REQUEST_TIMEOUT)
            api_response_contents = api_response.content.decode('utf-8')
            if api_response.status_code == status.HTTP_200_OK:
                return self.parse_response(api_response_contents)
            else:
                return {}

        except Exception as e:
            return {}
            #raise GenericException(status_type=STATUS_TYPE["APP"], exception_code=NONRETRYABLE_CODE["BAD_REQUEST"],
            #                       detail=repr(e), request=self.request)
