from . import services
from .api_client import ApiClient

class Client(object):
    """Client for interacting with the Tesoro API.

    Instantiate a client object with your access token and environment, then
    use the resource methods to access the API.

    Args:
      access_token (str): TBD where to get this token.
      environment (str): Either 'sandbox' or 'live'.
      base_url (str): Manually set a base URL. Most people should use
        `environment` instead.
      raise_on_idempotency_conflict (bool): Configure refetching of conflicting resource

    Example:
      client = Client(access_token=ACCESS_TOKEN, environment='sandbox')
      for customer in client.customers.list():
          print '{} {}'.format(customer.family_name, customer.given_name)
    """

    def __init__(self, access_token=None, environment=None, base_url=None, raise_on_idempotency_conflict=False):
        if access_token is None:
            raise ValueError('No access_token provided')

        if environment is None and base_url is None:
            raise ValueError('No environment or base_url specified')

        base_url = base_url or self._environment_url(environment)
        self._api_client = ApiClient(base_url, access_token)
        self._raise_on_idempotency_conflict = raise_on_idempotency_conflict

    @property
    def customers(self):
        return services.CustomersService(self._api_client, 3, 0.5, self._raise_on_idempotency_conflict)

    @property
    def payments(self):
        return services.PaymentsService(self._api_client, 3, 0.5, self._raise_on_idempotency_conflict)

    def _environment_url(self, environment):
        environment_urls = { 
            'live': 'TBD',
            'sandbox': 'https://api-sandbox.tesoro.com',
        }

        if environment not in environment_urls:
            msg = 'Invalid environment "{env}", use one of {env_names}'.format(
                env=environment,
                env_names=', '.join(environment_urls.keys())
            )
            raise ValueError(msg)

        return environment_urls[environment]
