"""
This file contains a wrapper for an HL7 message with convenience functions.
"""
from hl7apy.parser import parse_message


class HL7Message:
    """
    Encapsulates an HL7 message.
    """
    def __init__(self, hl7_message):
        """
        Initialize using a message parsed with hl7 library.
        """
        self.hl7_message = hl7_message

    @staticmethod
    def from_string(txt):
        """
        Initialize a message from string.
        """
        txt = txt.replace('\n','\r')
        return HL7Message(parse_message(txt, find_groups=False))

    @staticmethod
    def from_file(path):
        """
        Initialize a message from a file.
        """
        with open(path) as f:
            txt = f.read().strip()
        return HL7Message.from_string(txt)

    def to_string(self):
        """
        Returns a string representation of the encapsulated HL7 message.
        """
        return self.hl7_message.to_er7().replace('\r', '\n')

    def __getitem__(self, index):
        """
        Index fields in the HL7 message using HL7Field as key. Can retrieve field or subfield values.
        """
        segments = self.hl7_message.children
        for segment in segments:
            if segment.name == index.segment:
                for field in segment.children:
                    if field.name == index.field_name:
                        if index.component > 0:
                            for component in field.children:
                                comp_name_parts = component.name.split('_')
                                component_name = field.name + '_' + comp_name_parts[1]
                                if component_name == index.component_name:
                                    return component.value
                            raise KeyError('Component {} does not exist'.format(index.component_name))
                        return field.value
        raise KeyError('Could not retrieve {}'.format(index))

    def __setitem__(self, index, value):
        def set_component_value(field, index, value):
            if index.component > 0:
                for component in field.children:
                    comp_name_parts = component.name.split('_')
                    component_name = field.name + '_' + comp_name_parts[1]
                    if component_name == index.component_name:
                        component = value
                        return True

            # insert component value in the right position
            component_separator = self.hl7_message.encoding_chars['COMPONENT']
            comp_values = [c.value for c in field.children]
            if index.component == 0:
                str_value = value
            else:
                pre = comp_values + ['']*(index.component - len(comp_values)+1)
                str_value = component_separator.join(pre[:index.component-1] + [value] + comp_values[index.component-1:])
            field.value = str_value
            return True

        def set_field_value(segment, index, value):
            for field in segment.children:
                if field.name == index.field_name:
                    res = set_component_value(field, index, value)
                    if res:
                        return True
                    field = value
                    return True

            field = segment.add_field(index.field_name)
            set_component_value(field, index, value)
            return True

        res = False
        segments = self.hl7_message.children
        for segment in segments:
            if segment.name == index.segment:
                res = set_field_value(segment, index, value)
                break

        if not res:
            segment = self.hl7_message.add_segment(index.segment)
            res = set_field_value(segment, index, value)
