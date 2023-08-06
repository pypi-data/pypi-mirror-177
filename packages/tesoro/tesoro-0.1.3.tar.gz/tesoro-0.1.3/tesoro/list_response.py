class ListResponse(object):

    def __init__(self, records, api_response):
        self.records = records
        self.api_response = api_response

    @property
    def before(self):
        return self.api_response.body['meta']['cursors']['before']

    @property
    def after(self):
        return self.api_response.body['meta']['cursors']['after']
