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
        public_object_search_request.properties = list(self.extract_inner_properties())
        return self.fetch_all(self.hubspot_client.crm.line_items, public_object_search_request)

    def extract_inner_properties(self):
        if "properties" in self.schema:
            outer_properties = self.schema["properties"]
            if "properties" in outer_properties:
                inner_properties = outer_properties["properties"]
                return list(inner_properties["properties"].keys())
        return []
