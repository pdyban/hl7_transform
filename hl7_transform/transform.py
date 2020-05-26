"""
This file contains the transformation class.
"""

class HL7Transform:
    def __init__(self, mapping):
        """
        \param mapping A dictionary that contains field mappings.
        """
        self.mapping = mapping
