"""
This field contains definition of an HL7 field.
"""

class HL7Field:
    def __init__(self, name):
        self.name = name
        count = self.name.count('.')
        while count < 2:
            self.name += '.1'
            count += 1
        self.segment, self.field, self.sub_field = self.name.split('.', 3)

    def __repr__(self):
        return '({})'.format(self.name)

    def __str__(self):
        return '({})'.format(self.name)
