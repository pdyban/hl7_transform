from hl7_transform.cli import main_cli
# from hl7_transform.mapping import HL7Mapping
# from hl7_transform.transform import HL7Transform
# from hl7_transform.message import HL7Message
import unittest
import os
# import subprocess


class TestCLI(unittest.TestCase):
    def setUp(self):
        class Args:
            mappingfile = None
            message = None
            outfile = None

        self.args = Args()
        self.args.mappingfile = 'hl7_transform/test/test_transform.json'
        self.args.message = 'hl7_transform/test/msg2.hl7'
        self.args.outfile = 'test.hl7'
        self.args.type = 'json'

    def tearDown(self):
        if os.path.exists(self.args.outfile):
            os.remove(self.args.outfile)

    # TODO: fix this test case. It fails with error "/usr/bin/python: Import by filename is not supported"
    # def test_cli(self):
    #     cli = ["python", "-m hl7_transform {} {} {}".format(self.args.message, self.args.mappingfile, self.args.outfile)]
    #     res = subprocess.run(cli)
    #     print(res.returncode)
    #     self.assertEqual(0, res.returncode)
    #
    #     # verify result file
    #     mapping = HL7Mapping.from_json(self.args.mappingfile)
    #     message = HL7Message.from_file(self.args.message)
    #     transform = HL7Transform(mapping)
    #     expected_result_message = transform.execute(message)
    #     self.assertTrue(os.path.exists(self.args.outfile), msg='CLI call to library failed, the test message could not be transformed.')
    #     with open(self.args.outfile) as f:
    #         result_file = f.read()
    #         self.assertEqual(result_file, expected_result_message.to_string())

    def test_main_cli(self):
        res = main_cli(self.args)
        self.assertIsNone(res, msg='CLI failed')

    def test_main_cli_csv_mapping(self):
        self.args.mappingfile = 'hl7_transform/test/test_transform.csv'
        self.args.type = 'csv'
        res = main_cli(self.args)
        self.assertIsNone(res, msg='CLI failed')
