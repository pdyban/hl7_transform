"""
Tests for hl7_transform.mapping module.
"""
import unittest
from hl7_transform.mapping import HL7Mapping


class TestHL7Mapping(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_from_json(self):
        mapping = HL7Mapping.from_json('hl7_transform/test/test_transform.json')
        self.assertEqual(len(mapping), 13)

    def test_from_string_json(self):
        with open('hl7_transform/test/test_transform.json') as f:
            mapping = HL7Mapping.from_string(f.read())
        self.assertEqual(len(mapping), 13)

    def test_from_csv(self):
        mapping = HL7Mapping.from_csv('hl7_transform/test/test_transform.csv')
        self.assertEqual(len(mapping), 42)

        expected_result = [
            {'target_field_name': 'PID.3', 'operation_name': 'SetValue'},
            {'target_field_name': 'PID.18', 'operation_name': 'SetValue'},
        ]
        for index, exp_res in enumerate(expected_result):
            target_field = list(mapping[index].keys())[0]
            operation = mapping[index][target_field]
            self.assertEqual(target_field.name, exp_res['target_field_name'])
            self.assertEqual(operation.__class__.__name__, exp_res['operation_name'])
        expected_result = [{
            'target_field_name': 'PV1.2',
            'operation_name': 'CopyValue',
            'source_field': 'PID.18'}]
        index = 2
        exp_res = expected_result[0]
        target_field = list(mapping[index].keys())[0]
        operation = mapping[index][target_field]
        self.assertEqual(target_field.name, exp_res['target_field_name'])
        self.assertEqual(operation.__class__.__name__, exp_res['operation_name'])
        self.assertEqual(operation.field.name, exp_res['source_field'])


if __name__ == '__main__':
    unittest.main()
