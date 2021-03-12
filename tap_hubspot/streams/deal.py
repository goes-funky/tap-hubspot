from hubspot.crm.deals import Filter, FilterGroup, PublicObjectSearchRequest

from .base import Resource


class Deal(Resource):
    # code is the same as the product but the
    # Filter, FilterGroup, PublicObjectSearchRequest are imported from
    # a different package
    tap_stream_id = "deals"
    key_properties = ["id"]
    replication_key = "created_at"
    replication_method = "INCREMENTAL"

    def get_data(self, value):
        filter = Filter(property_name="createdate", operator="GT", value=value)
        filter_group = FilterGroup(filters=[filter])
        public_object_search_request = PublicObjectSearchRequest(
            filter_groups=[filter_group]
        )
        return self.fetch_all(self.hubspot_client.crm.deals, public_object_search_request)

    def extract_inner_properties(self):
        if "properties" in self.schema:
            properties = self.schema["properties"].keys()
            return properties
        return []

    def convert_obj(self, obj):
        new_obj = obj["properties"]
        new_obj["id"] = obj["id"]
        new_obj["archived"] = obj["archived"]
        new_obj["created_at"] = obj["created_at"]
        return new_obj

    def get_hubspot_object(self):
        return self.hubspot_client.crm.deals
