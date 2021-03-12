from hubspot.crm.line_items import Filter, FilterGroup, PublicObjectSearchRequest

from .base import Resource


class LineItem(Resource):
    # code is the same as the product but the
    # Filter, FilterGroup, PublicObjectSearchRequest are imported from
    # a different package
    tap_stream_id = "line_items"
    key_properties = ["id"]
    replication_key = "created_at"
    replication_method = "INCREMENTAL"

    def get_hubspot_object(self):
        return self.hubspot_client.crm.line_items
