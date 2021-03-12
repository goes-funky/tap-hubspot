from tap_hubspot.streams.association_resource import Associations
from .deal import Deal


class DealByCompany(Associations):
    tap_stream_id = "deal_by_companies"

    first_resource_name = "DEALS"
    second_resource_name = "COMPANIES"

    def get_first_resource(self):
        return Deal(hubspot_client=self.hubspot_client)
