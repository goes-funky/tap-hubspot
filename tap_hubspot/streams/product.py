from .base import Resource

class Product(Resource):
    tap_stream_id = "products"
    key_properties = ["id"]
    replication_key = "created_at"
    replication_method = "INCREMENTAL"

    def get_hubspot_object(self):
        return self.hubspot_client.crm.products
