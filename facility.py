from childcare_service_api import ChildcareServiceApi
from datetime import datetime

class Facility(object):

    def __init__(self, facility_id):
        self.facility_id = facility_id
        self.cs_api = ChildcareServiceApi()

    @staticmethod
    def crawl_facilities(limit=None):
        cs_api = ChildcareServiceApi()
        page_num = 1
        while True:
            response = cs_api.get_child_facility_list(page_num)
            print(response)
            break

    def crawl_facility_info(self):
        response = self.cs_api.get_child_facility_item(self.facility_id)

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
        self.accident_insurance = True if info.AccientInsurance == 'Y' else False
        self.fire_insurance = True if info.FireInsurance == 'Y' else False
        self.compensation_insurance = True if info.CompensationInsurance == 'Y' else False

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

