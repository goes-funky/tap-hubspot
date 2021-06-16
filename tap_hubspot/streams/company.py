from .base import Resource


# only used for the events not for getting company, v1 is used to get the companies
class Company(Resource):
    tap_stream_id = "companies"
    key_properties = ["id"]
    replication_key = "created_at"
    replication_method = "INCREMENTAL"

    def get_hubspot_object(self):
        return self.hubspot_client.crm.companies
