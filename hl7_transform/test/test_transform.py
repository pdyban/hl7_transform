"""
Tests for hl7_transform.transform module.
"""
import unittest
from hl7_transform.mapping import HL7Mapping
from hl7_transform.transform import HL7Transform
from hl7_transform.message import HL7Message
from hl7_transform.field import HL7Field


class TestHL7Transform(unittest.TestCase):
    def setUp(self):
        mapping = HL7Mapping.from_json('hl7_transform/test/test_transform.json')
        # using example message from hl7 library (readthedocs)
        self.message = HL7Message.from_file('hl7_transform/test/msg2.hl7')
        self.transform = HL7Transform(mapping)

    def tearDown(self):
        pass

    def test_initialization(self):
        self.assertEqual(len(self.transform.mapping), 6)

    def test_execution(self):
        message_transformed = self.transform.execute(self.message)
        self.assertEqual(len(message_transformed.hl7_message.children), 7)
        self.assertTrue('TQ1' in [segment.name for segment in message_transformed.hl7_message.children])
        self.assertEqual(message_transformed[HL7Field('MSH.9')], 'SIU^S12^SIU_S12')
        self.assertEqual(message_transformed[HL7Field('NTE.3')], 'Muss Ultraschall bekommen')
        with self.assertRaises(KeyError):
            message_transformed[HL7Field('NTE.4')]
        self.assertEqual(len(message_transformed[HL7Field('MSH.5')]), 0)
        self.assertEqual(message_transformed[HL7Field('TQ1.7')], '202005201615')
        self.assertEqual(message_transformed[HL7Field('TQ1.8')], '202005201635')
        self.assertEqual(message_transformed[HL7Field('TQ1.9')], '202005201615 + 20')

    def test_message_to_string(self):
        # TODO: move to test_message.py
        self.assertIn('\n', self.message.to_string())


if __name__ == '__main__':
    unittest.main()
