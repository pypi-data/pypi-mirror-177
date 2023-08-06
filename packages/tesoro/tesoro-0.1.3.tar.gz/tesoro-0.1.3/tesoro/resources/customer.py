class Customer(object):
    """A thin wrapper around a customer, providing easy access to its
    attributes.

    Example:
      customer = client.customers.get()
      customer.id
    """

    def __init__(self, attributes, api_response):
        self.attributes = attributes
        self.api_response = api_response

    @property
    def created_at(self):
        return self.attributes.get('created_at')

    @property
    def customer_reference(self):
        return self.attributes.get('customer_reference')

    @property
    def email(self):
        return self.attributes.get('email')

    @property
    def given_name(self):
        return self.attributes.get('given_name')

    @property
    def first_family_name(self):
        return self.attributes.get('first_family_name')

    @property
    def second_family_name(self):
        return self.attributes.get('second_family_name')

    @property
    def business_name(self):
        return self.attributes.get('business_name')

    @property
    def national_id_number(self):
        return self.attributes.get('national_id_number')
