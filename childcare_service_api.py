import logging

from suds.client import Client
from settings import CHILDCARE_SERVICE_KEY

logger = logging.getLogger(__name__)


class ChildcareServiceApi(object):

    def __init__(self):
        url = "https://s3-ap-northeast-1.amazonaws.com" \
            "/nursery.novice.io/ReservateChildcareService.xml"
        self.client = Client(url)
        common_msg = self.client.factory.create('ComMsgHeaderRequest')
        common_msg.ServiceKey = CHILDCARE_SERVICE_KEY
        self.client.set_options(soapheaders=common_msg)

    def get_child_facility_item(self, search_kind, facility_id):
        logger.debug("Get child facility item : search_kind=%s, facility_id=%s", search_kind, facility_id)
        result = self.client.service.ChildFacilityItem("01", facility_id)
        return result

    def get_child_facility_list(self, search_kind, page_num):
        logger.debug("Get child facility list : search_kind=%s, page_num=%s", search_kind, page_num)
        result = self.client.service.ChildFacilityList(
            SearchKind="01", PageNum=page_num
        )
        return result

    def get_application_waiting_result_item(self):
        pass
