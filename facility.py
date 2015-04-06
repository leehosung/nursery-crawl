import logging
from datetime import datetime
import sys
from time import sleep

from boto.dynamodb2.table import Table
from boto.dynamodb2.items import Item
from boto.dynamodb2.exceptions import ItemNotFound


from childcare_service_api import ChildcareServiceApi

logger = logging.getLogger(__name__)


class Facility(object):

    cs_api = ChildcareServiceApi()
    search_kind = "01"
    table_name = "facility"

    def __init__(self, facility_id):
        self.facility_id = int(facility_id)
        self.facility_name = ''

    def __str__(self):
        return "[%s] %s" % (self.facility_id, self.facility_name)

    @classmethod
    def get_all_facilities(cls, connection=None):
        table = Table(cls.table_name, connection=connection)
        return list(table.scan())

    @classmethod
    def crawl_facilities(cls, limit=sys.maxsize, connection=None):
        page_num = 1
        count = 1
        while True:
            r = cls.cs_api.get_child_facility_list(cls.search_kind, page_num)
            for f in r.ChildFacilityList:
                facility = cls(f.FacilityID)
                facility.update_from_list(f)
                facility.save(connection=connection)
                logger.debug(
                    "Get facility from list API : facility=%s", facility
                )
                yield facility
                if limit <= count:
                    break
                else:
                    count += 1
                    # To avoid dynamodb write limit
                    sleep(0.5)
            if r.TotalPageNumber == r.PageNumber or limit <= count:
                break
            else:
                page_num += 1

    def update_from_list(self, info):
        self.facility_name = info.FacilityName
        self.certification = True if info.Certification == 'Y' else False
        self.seoul = True if info.Seoul == 'Y' else False
        self.cr_type = info.Type
        self.waiting_entrance = info.WaitingEnterance
        self.fixed_number = info.FixedNumber
        self.present_number = info.PresentNumber
        self.telephone = info.Telephone
        self.fax = info.Fax.strip()
        self.address = ' '.join(info.Address.split())
        self.updated = datetime.now()

    def crawl_facility_info(self):
        response = Facility.cs_api.get_child_facility_item(self.search_kind, self.facility_id)

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
        if hasattr(response, 'ChildFacilityPhoto'):
            photos = response.ChildFacilityPhoto
            self.photos = []
            for k, v in photos:
                self.photos.append(v)

        self.detail_updated = datetime.now()

        logger.debug(
            "Get facility from detail API : facility=%s", self
        )

    def save(self, connection=None):
        data = self.__dict__
        for k, v in data.items():
            if type(v) == datetime:
                data[k] = v.isoformat()
        table = Table(self.table_name, connection=connection)
        try:
            item = table.get_item(facility_id=self.facility_id)
        except ItemNotFound:
            table.put_item(data=data, overwrite=True)
        else:
            for k, v in data.items():
                item[k] = v
            item.save()


class Nursery(Facility):
    search_kind = "01"
    table_name = "nursery"
