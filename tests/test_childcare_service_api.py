import unittest
from childcare_service_api import ChildcareServiceApi


class ChildcareServiceApiTestCase(unittest.TestCase):

    def setUp(self):
        self.api = ChildcareServiceApi()

    def test_get_child_facility_item(self):
        facility = self.api.get_child_facility_item("01", 11110000042)
        self.assertEqual("효자어린이집", facility.ChildFacilityInfo.FacilityName)
        self.assertIn('ChildFacilityWaiting', facility)
        self.assertIn('ChildcarePrice', facility)

    def test_get_child_facility_list(self):
        facility_list = self.api.get_child_facility_list("01", 1)
        self.assertIn('TotalFacilifyCount', facility_list)
        self.assertIn('TotalPageNumber', facility_list)

    def test_get_application_waiting_result_item(self):
        pass

if __name__ == '__main__':
    unittest.main()
