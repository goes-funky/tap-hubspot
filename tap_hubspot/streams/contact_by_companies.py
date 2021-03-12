from tap_hubspot.streams.association_resource import Associations
from .contact import Contact


class ContactByCompany(Associations):
    tap_stream_id = "contact_by_companies"

    first_resource_name = "CONTACTS"
    second_resource_name = "COMPANIES"

    def get_first_resource(self):
        return Contact(hubspot_client=self.hubspot_client)
