import singer
from abc import abstractmethod
from .base import Resource
from hubspot import HubSpot

from .contact import Contact
from tenacity import retry_if_exception_type, retry, wait_fixed, stop_after_attempt

from .deal import Deal
from .product import Product

LOGGER = singer.get_logger()


class Event(Resource):
    replication_key_in_obj = False

    def get_data(self, value):
        results = []
        for parent_obj in self.get_parent().get_data(value):
            LOGGER.info("Getting events for object {}".format(parent_obj.id))
            after = None
            while True:
                page = self.call_api(object_type=self.get_object_type(), object_id=parent_obj.id, after=after)
                results.extend(page.results)
                if page.paging is None:
                    break
                after = page.paging.next.after
        return results

    @retry(wait=wait_fixed(5), retry=retry_if_exception_type(Exception), stop=stop_after_attempt(10))
    def call_api(self, **kwargs):
        return self.get_hubspot_object().events_api.get_page(**kwargs)

    def get_hubspot_object(self):
        return self.hubspot_client.events

    @abstractmethod
    def get_parent(self) -> Resource:
        raise Exception("get_parent is not implemented")

    def get_object_type(self):
        raise Exception("get_object_type is not implemented")


class ContactEvent(Event):
    def get_parent(self) -> Resource:
        return Contact(hubspot_client=self.hubspot_client)

    def get_object_type(self):
        return 'contact'


class DealEvent(Event):
    def get_parent(self) -> Resource:
        return Deal(hubspot_client=self.hubspot_client)

    def get_object_type(self):
        return 'deal'


class ProductEvent(Event):
    def get_parent(self) -> Resource:
        return Product(hubspot_client=self.hubspot_client)

    def get_object_type(self):
        return 'product'
