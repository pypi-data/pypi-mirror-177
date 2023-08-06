from office365.runtime.client_result import ClientResult
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.base_entity import BaseEntity
from office365.sharepoint.search.simple_data_table import SimpleDataTable


class DocumentCrawlLog(BaseEntity):
    """This object contains methods that can be used by the protocol client to retrieve information
    about items that were crawled."""

    def __init__(self, context):
        static_path = ResourcePath("Microsoft.SharePoint.Client.Search.Administration.DocumentCrawlLog")
        super(DocumentCrawlLog, self).__init__(context, static_path)

    def get_crawled_urls(self, get_count_only=False):
        """
        Retrieves information about all the contents that were crawled.

        :type get_count_only: bool
        """
        return_type = ClientResult(self.context, SimpleDataTable())
        payload = {
            "getCountOnly": get_count_only
        }
        qry = ServiceOperationQuery(self, "GetCrawledUrls", None, payload, None, return_type)
        self.context.add_query(qry)
        return return_type

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Client.Search.Administration.DocumentCrawlLog"
