from hubspot.crm.products import Filter, FilterGroup, PublicObjectSearchRequest

from .base import Resource


class Product(Resource):

    def get_data(self, value):
        filter = Filter(property_name="createdate", operator="GT", value=value)
        filter_group = FilterGroup(filters=[filter])
        public_object_search_request = PublicObjectSearchRequest(
            filter_groups=[filter_group]
        )
        return self.fetch_all(self.hubspot_client.crm.products, public_object_search_request)
