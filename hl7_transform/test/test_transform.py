"""
Tests for hl7_transform.transform module.
"""
import unittest
from hl7_transform.mapping import HL7Mapping
from hl7_transform.transform import HL7Transform
import json


class TestHL7Transform(unittest.TestCase):
    def setUp(self):
        mapping = HL7Mapping.from_json('hl7_transform/test/test_transform.json')
        self.transform = HL7Transform(mapping)

    def tearDown(self):
        pass

    def test_initialization(self):
        self.assertEqual(len(self.transform.mapping), 1)
        pass


if __name__ == '__main__':
    unittest.main()
