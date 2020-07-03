"""
Encapsulates the functionality of an HL7 field.
"""

class HL7Field:
    def __init__(self, name):
        self.name = name
        count = name.count('.')
        if count < 2:
            name += '.0'
        self.segment, self.field, self.component = name.split('.', 3)
        self.field = int(self.field)
        self.repetition = 1  # currently fixed
        self.component = int(self.component)
        self.sub_component = 1  # currently fixed

    def __repr__(self):
        return '({})'.format(self.name)

    def __str__(self):
        return '({})'.format(self.name)

    @property
    def field_name(self):
        return '{}_{}'.format(self.segment, self.field)

    @property
    def component_name(self):
        return '{}_{}_{}'.format(self.segment, self.field, self.component)
