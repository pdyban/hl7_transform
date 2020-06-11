"""
This file contains functions to create and persist HL7 field mappings.
"""
import json
from hl7_transform.field import HL7Field
from hl7_transform.operations import HL7Operation


def my_hook(dct):
    """
    Convert items in JSON dictionary from string to HL7Field.
    """
    ret = {}
    operation_name, source_fields, args = dct['operation'], dct.get('source_fields', [dct.get('source_field', None)]), dct.get('args', [])
    if len(source_fields) == 1 and source_fields[0] is None:
        source_fields = []
    ret[HL7Field(dct['target_field'])] = HL7Operation.from_name(operation_name, source_fields, args)
    return ret


# class HL7JsonDecoder(json.JSONDecoder):
#     """
#     Custom JSON decoder that parses all fields to HL7Field objects.
#     """
#     def __init__(self):
#         json.JSONDecoder.__init__(self, object_hook=my_hook)


class HL7Mapping(list):
    """
    Contains field mappings and rules how to map fields.
    """
    @staticmethod
    def from_json(path):
        """
        Initialize mapping from a JSON file.
        \param path Path to JSON file.
        """
        with open(path) as f:
            js = json.load(f, object_hook=my_hook)
        return HL7Mapping(js)

    def __repr__(self):
        ret = []
        for mapping in self:
            for target_field, operation in mapping.items():
                ret.append('{} will contain the result of {}'.format(target_field, operation))
        return '\n'.join(ret)
