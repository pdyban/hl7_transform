from hl7_transform.message import HL7Message
from hl7_transform.field import HL7Field
import unittest


class TestHL7Transform(unittest.TestCase):
    def setUp(self):
        self.message = HL7Message.from_file('hl7_transform/test/test_msg.hl7')

    def test_message_accessor(self):
        self.assertEqual(self.message[HL7Field('MSH.9')], 'SIU^S12')
        self.assertEqual(self.message[HL7Field('MSH.9.1')], 'SIU')
        self.assertEqual(self.message[HL7Field('MSH.9.2')], 'S12')
        with self.assertRaises(KeyError):
            self.message[HL7Field('MSH.9.3')]

    def test_message_to_string(self):
        self.assertIn('\n', self.message.to_string())


if __name__ == '__main__':
    unittest.main()
