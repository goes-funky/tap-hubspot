import attr
from .base import Resource
from hubspot.crm.associations import BatchInputPublicObjectId, PublicObjectId
from hubspot.crm.associations import BatchInputPublicObjectId, PublicObjectId
import hubspot

from .deal import Deal

PAGE_MAX_SIZE = 100


@attr.s
class Associations(Resource):
    first_resource_name = attr.ib(default="DEALS")
    second_resource_name = attr.ib(default="COMPANIES")
    replication_key_in_obj = False

    def get_data(self, value):
        first_resource = self.get_resource_company(self.first_resource_name)
        data = first_resource.get_data(value)
        ids = self.extract_ids(data)
        chunks = self.chunks(ids, 100)
        data = []
        for chunk in chunks:
            batch_input_public_object_id = BatchInputPublicObjectId(
                inputs=chunk
            )
            results = self.fetch_all(self.hubspot_client.crm.associations, batch_input_public_object_id)
            data.extend(results)
        return data

    def get_resource_company(self, name):
        dict_resource = {
            "DEALS": Deal(hubspot_client=self.hubspot_client)
        }
        return dict_resource[name]

    def fetch_all(self, resource, public_object_search_request, **kwargs):
        page = resource.batch_api.read(
            self.first_resource_name,
            self.second_resource_name,
            batch_input_public_object_id=public_object_search_request
        )

        return page.results

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
