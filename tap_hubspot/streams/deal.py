from hubspot.crm.deals import Filter, FilterGroup, PublicObjectSearchRequest

from .base import Resource


class Deal(Resource):
    # code is the same as the product but the
    # Filter, FilterGroup, PublicObjectSearchRequest are imported from
    # a different package
    dynamic_columns = ["hs_date_entered_", "hs_date_exited_", "hs_time_in_"]
    include_parameters = ["hs_date_entered_closedwon", "hs_date_exited_closedwon"]

    def get_data(self, value):
        filter = Filter(property_name="createdate", operator="GT", value=value)
        filter_group = FilterGroup(filters=[filter])
        public_object_search_request = PublicObjectSearchRequest(
            filter_groups=[filter_group]
        )

        properties = self.extract_inner_properties()
        public_object_search_request.properties = properties
        public_object_search_request.properties = self.include_parameters + list(properties)
        return self.fetch_all(self.hubspot_client.crm.deals, public_object_search_request)

    def extract_inner_properties(self):
        if "properties" in self.schema:
            outer_properties = self.schema["properties"]
            if "properties" in outer_properties:
                inner_properties = outer_properties["properties"]
                return inner_properties["properties"].keys()
        return []

    def convert_obj(self, obj):
        properties = obj["properties"]
        for dynamic_col in self.dynamic_columns:
            obj[dynamic_col[:-1]] = [{"value": properties[k],
                                      "id": k.replace(dynamic_col, "")}
                                     for k in properties if
                                     k.startswith(dynamic_col) and k not in self.include_parameters]

        return obj
