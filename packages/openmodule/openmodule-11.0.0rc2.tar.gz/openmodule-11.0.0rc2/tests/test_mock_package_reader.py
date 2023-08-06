from unittest import TestCase

from openmodule_test.package_reader import MockPackageReader


class MockPackageReaderTest(TestCase):
    def setUp(self) -> None:
        self.reader = MockPackageReader()
        self.services = self.reader.services

    def test_parent_is_set_correctly(self):
        self.services.add_hardware_package("hw_compute_nuc_1", hardware_type=["compute"], ip="10.15.0.200")
        self.services.add_software_package("om_fancy_assistant_1", parent="hw_compute_nuc_1",
                                           env={"LOG_LEVEL": " DEBUG"})

        self.assertIsNotNone(self.reader.get_service_by_name("hw_compute_nuc_1"))
        self.assertIsNotNone(self.reader.get_service_by_name("om_fancy_assistant_1"))
        self.assertIsNotNone(self.reader.get_service_by_name("om_fancy_assistant_1").parent)
        self.assertEqual("hw_compute_nuc_1", self.reader.get_service_by_name("om_fancy_assistant_1").parent.name)

        # fake-uninstall the service, the parent must be gone
        self.services.remove("hw_compute_nuc_1")
        self.assertIsNone(self.reader.get_service_by_name("om_fancy_assistant_1").parent)
