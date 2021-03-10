from tap_hubspot.streams.association_resource import Associations


class DealByCompany(Associations):
    tap_stream_id = "deals_by_company"
    key_properties = ["id"]
    replication_key = "created_at"
    replication_method = "INCREMENTAL"

    first_resource_name = "DEALS"
    second_resource_name = "COMPANIES"
