"""
This file contains functions to create and persist HL7 field mappings.
"""
import json


class HL7Mapping(dict):
    @staticmethod
    def from_json(path):
        """
        Initialize mapping from a JSON file.
        \param path Path to JSON file.
        """
        with open(path) as f:
            js = json.load(f)
        return HL7Mapping(js)
