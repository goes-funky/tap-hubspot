import attr
from .base import Resource
from hubspot.crm.associations import BatchInputPublicObjectId, PublicObjectId
from hubspot.crm.associations import BatchInputPublicObjectId, PublicObjectId
import hubspot

from .deal import Deal
import abc

PAGE_MAX_SIZE = 100


class Associations(Resource):
    first_resource_name = None
    second_resource_name = None
    replication_key_in_obj = False

    def get_data(self, value):
        first_resource = self.get_first_resource()
        parent_data = first_resource.get_data(value)
        ids = self.extract_ids(parent_data)
        chunks = self.chunks(ids, 100)
        data = []
        for chunk in chunks:
            batch_input_public_object_id = BatchInputPublicObjectId(
                inputs=chunk
            )
            results = self.fetch_all(self.hubspot_client.crm.associations, batch_input_public_object_id)
            data.extend(results)
        return data

    def fetch_all(self, resource, public_object_search_request, **kwargs):
        page = resource.batch_api.read(
            self.first_resource_name,
            self.second_resource_name,
            batch_input_public_object_id=public_object_search_request
        )

        return page.results

    @abc.abstractmethod
    def get_first_resource(self):
        return Deal(hubspot_client=self.hubspot_client)

    @staticmethod
    def extract_ids(data):
        ids = []
        for obj in data:
            ids.append(PublicObjectId(id=obj.id))
        return ids

    @staticmethod
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def get_hubspot_object(self):
        pass
