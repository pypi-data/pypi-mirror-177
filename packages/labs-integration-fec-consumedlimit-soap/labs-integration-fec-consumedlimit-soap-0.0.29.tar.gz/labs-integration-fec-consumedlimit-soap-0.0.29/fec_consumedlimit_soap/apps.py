from django.apps import AppConfig


class FecConsumedlimitSoapConfig(AppConfig):
    # This name needs to be added to the installed apps section of the settings.py
    name = 'fec_consumedlimit_soap'
    verbose_name = 'FEC Consumed Limit SOAP'

    # This key is used to identify the apps for Kuliza Labs Integration Broker.
    labs_integration_app = True

    # This key is used to define a prefix for all URL in the app.
    # This will only be honoured when the key 'labs_integration_app' is 'True'.
    labs_url_prefix = '/fec/consumedlimit/soap/'
