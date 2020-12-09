import attr
import abc

PAGE_MAX_SIZE = 100


@attr.s
class Stream(object):
    tap_stream_id = attr.ib()
    sync = attr.ib()
    key_properties = attr.ib()
    replication_key = attr.ib()
    replication_method = attr.ib()

    schema = {}

    def set_schema(self, schema):
        self.schema = schema


@attr.s
class Resource(Stream):
    hubspot_client = attr.ib(default=None)

    @abc.abstractmethod
    def get_data(self, value):
        return []

    @staticmethod
    def fetch_all(resource, public_object_search_request, **kwargs):

        results = []
        after = None

        while True:
            public_object_search_request.limit = PAGE_MAX_SIZE
            public_object_search_request.after = after
            page = resource.search_api.do_search(public_object_search_request)
            results.extend(page.results)
            if page.paging is None:
                break
            after = page.paging.next.after

        return results

    def convert_obj(self, obj):
        return obj
