"""
Tests for hl7_transform.mapping module.
"""
import unittest
from hl7_transform.mapping import HL7Mapping
import json

class TestHL7Mapping(unittest.TestCase):
    def setUp(self):
        self.mapping = HL7Mapping.from_json('hl7_transform/test/test_transform.json')

    def tearDown(self):
        pass

    def test_initialization(self):
        self.assertEqual(len(self.mapping), 6)


if __name__ == '__main__':
    unittest.main()
