from hubspot.crm.contacts import Filter, FilterGroup, PublicObjectSearchRequest

from .base import Resource


class Contact(Resource):
    # code is the same as the product but the
    # Filter, FilterGroup, PublicObjectSearchRequest are imported from
    # a different package
    tap_stream_id = "contacts"
    key_properties = ["id"]
    replication_key = "created_at"
    replication_method = "INCREMENTAL"

    def get_data(self, value):
        filter = Filter(property_name="createdate", operator="GT", value=value)
        filter_group = FilterGroup(filters=[filter])
        public_object_search_request = PublicObjectSearchRequest(
            filter_groups=[filter_group]
        )

        return self.fetch_all(self.hubspot_client.crm.contacts, public_object_search_request)

    def extract_inner_properties(self):
        if "properties" in self.schema:
            properties = self.schema["properties"].keys()
            return properties
        return []
