import logging
from datetime import datetime

from childcare_service_api import ChildcareServiceApi

logger = logging.getLogger(__name__)


class Facility(object):

    cs_api = ChildcareServiceApi()

    def __init__(self, facility_id):
        self.facility_id = int(facility_id)

    @staticmethod
    def crawl_facilities(limit=None):
        page_num = 1
        count = 1
        while True:
            r = Facility.cs_api.get_child_facility_list(page_num)
            for f in r.ChildFacilityList:
                facility = Facility(f.FacilityID)
                facility.crawl_facility_info()
                yield facility
                count += 1
            if r.TotalPageNumber == r.PageNumber or limit == count:
                break

    def crawl_facility_info(self):
        logger.debug(
            "Get facility info using API : facility_id=%d", self.facility_id
        )
        response = Facility.cs_api.get_child_facility_item(self.facility_id)

        # ChildFacilityInfo
        info = response.ChildFacilityInfo
        self.facility_name = info.FacilityName
        self.cr_type = info.CRType
        self.cr_spec = info.CRSpec
        self.fixed_number = int(info.FixedNumber)
        self.present_number = int(info.PresentNumber)
        self.president_name = info.PresidentName
        self.open_date = datetime.strptime(info.OpenDate, "%Y-%m-%d")
        self.vehicle = True if info.Vehicle == 'Y' else False
        self.telephone = info.Telephone
        self.address = ' '.join(info.Address.split())
        self.gov_support = True if info.GovSupport == 'Y' else False
        self.accident_insurance = True \
            if info.AccientInsurance == 'Y' else False
        self.fire_insurance = True if info.FireInsurance == 'Y' else False
        self.compensation_insurance = True \
            if info.CompensationInsurance == 'Y' else False

        # ChildcarePrice
        prices = response.ChildcarePrice
        self.prices = dict()
        for k, v in prices:
            k = k.replace("Age", "").lower()
            self.prices[k] = int(v)

        # ChildFacilityWaiting
        child_facility_waiting = response.ChildFacilityWaiting
        self.waitings = dict()
        for k, v in child_facility_waiting:
            if k.startswith("Age"):
                k = k.replace("Age", "").lower()
                self.waitings[k] = int(v)
        self.reserv_confirm = child_facility_waiting.reservConfirm
        self.reserv_wait = child_facility_waiting.reservWait
        self.reserv_remain = child_facility_waiting.reservRemain
        self.reserv_regular = child_facility_waiting.reservRegular

        # ChildFacilityPhoto
        photos = response.ChildFacilityPhoto
        self.photos = []
        for k, v in photos:
            self.photos.append(v)
