from hl7_transform.__main__ import main_cli
import unittest
import os
from contextlib import redirect_stdout
import io


class TestCLI(unittest.TestCase):
    def setUp(self):
        class Args:
            mappingfile = None
            message = None
            out = None
            type = 'json'

            def __contains__(self, key):
                return key in self.__dict__ and self.__dict__[key] is not None

        self.args = Args()
        self.args.mappingfile = 'hl7_transform/test/test_transform.json'
        self.args.message = 'hl7_transform/test/test_msg.hl7'
        self.args.out = 'test.hl7'

    def tearDown(self):
        if self.args.out is not None and os.path.exists(self.args.out):
            os.remove(self.args.out)

    def test_main_cli(self):
        res = main_cli(self.args)
        self.assertIsNone(res, msg='CLI failed')

    def test_main_cli_csv_mapping(self):
        self.args.mappingfile = 'hl7_transform/test/test_transform.csv'
        self.args.type = 'csv'
        res = main_cli(self.args)
        self.assertIsNone(res, msg='CLI failed')

    def test_main_cli_new_message(self):
        self.args.message = None
        self.args.mappingfile = 'hl7_transform/test/test_transform_empty_message.json'
        res = main_cli(self.args)
        self.assertIsNone(res, msg='CLI failed')

    def test_main_cli_out(self):
        self.args.out = None
        s = io.StringIO()
        res = False
        with redirect_stdout(s):
            res = main_cli(self.args)
        self.assertIsNone(res, msg='CLI failed')
