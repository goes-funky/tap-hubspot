from hubspot.crm.products import Filter, FilterGroup, PublicObjectSearchRequest

from .base import Resource


class Product(Resource):
    search_key = "createdate"

    def get_data(self, value):
        filter = Filter(property_name="createdate", operator="GTE", value=value)
        filter_group = FilterGroup(filters=[filter])
        public_object_search_request = PublicObjectSearchRequest(
            filter_groups=[filter_group]
        )
        return self.fetch_all(self.object_resource, public_object_search_request)
