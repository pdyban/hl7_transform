"""
This file contains functions to create and persist HL7 field mappings.
"""
import json
import csv
from hl7_transform.field import HL7Field
from hl7_transform.operations import HL7Operation


def my_hook(dct):
    """
    Convert items in JSON dictionary from string to HL7Field.
    """
    ret = {}
    if 'operation' in dct and 'target_field' in dct:
        operation_name, source_fields, args = dct['operation'], dct.get('source_fields', [dct.get('source_field', None)]), dct.get('args', {})
        if len(source_fields) == 1 and source_fields[0] is None:
            source_fields = []
        ret[HL7Field(dct['target_field'])] = HL7Operation.from_name(operation_name, source_fields, args)
    else:
        for key, value in dct.items():
            ret[key] = value
    return ret


class HL7Mapping(list):
    """
    Contains field mappings and rules how to map fields.
    """
    @staticmethod
    def from_json(path):
        """
        Initialize mapping from a JSON file.
        :param path: Path to JSON file.
        """
        with open(path) as f:
            js = json.load(f, object_hook=my_hook)
        return HL7Mapping(js)

    @staticmethod
    def from_csv(path):
        """
        Initialize mapping from a CSV file.
        :param path: Path to CSV file.

        The header line of the CSV file should contain the field names, e.g.::

            target_field;operation;args.value
            PID.3;set_value;123^^^DOCTOLIB^PI
        """
        js = []
        with open(path) as csv_file:
            reader = csv.DictReader(csv_file)
            for line in reader:
                dic = {}
                for key, value in line.items():
                    if '.' in key:
                        key, subkey = key.split('.', 2)
                        sub = {}
                        sub[subkey] = value
                        dic[key] = sub
                    else:
                        dic[key] = value
                js.append(dic)
        js = json.loads(json.dumps(js), object_hook=my_hook)

        return HL7Mapping(js)

    @staticmethod
    def from_string(s):
        """Read mapping scheme from a JSON-formatted string"""
        js = json.loads(s, object_hook=my_hook)
        return HL7Mapping(js)

    def __str__(self):
        ret = []
        for mapping in self:
            for target_field, operation in mapping.items():
                ret.append('{} will contain the result of {}'.format(target_field, operation))
        return '\n'.join(ret)
