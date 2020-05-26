"""
This file contains functions to create and persist HL7 field mappings.
"""
import json
from hl7_transform.field import HL7Field


def my_hook(dct):
    """
    Convert items in JSOn dictionary from string to HL7Field.
    """
    ret = {}
    for key, value in dct:
        ret[HL7Field(key)] = HL7Field(value)
    return ret


class HL7JsonDecoder(json.JSONDecoder):
    """
    Custom JSON decoder that parses all fields to HL7Field objects.
    """
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_pairs_hook=my_hook, *args, **kwargs)


class HL7Mapping(dict):
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
            js = json.load(f, cls=HL7JsonDecoder)
        return HL7Mapping(js)

    def __repr__(self):
        ret = []
        for dst, src in self.items():
            ret.append('{} will contain the value of {}'.format(dst, src))
        return '\n'.join(ret)
