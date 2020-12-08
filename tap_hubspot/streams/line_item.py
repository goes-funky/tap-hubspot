from hubspot.crm.line_items import Filter, FilterGroup, PublicObjectSearchRequest

from .base import Resource


class LineItem(Resource):
    # code is the same as the product but the
    # Filter, FilterGroup, PublicObjectSearchRequest are imported from
    # a different package

    def get_data(self, value):
        filter = Filter(property_name="createdate", operator="GT", value=value)
        filter_group = FilterGroup(filters=[filter])
        public_object_search_request = PublicObjectSearchRequest(
            filter_groups=[filter_group]
        )
        return self.fetch_all(self.object_resource, public_object_search_request)
