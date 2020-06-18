"""
This file contains field operations.
"""

from hl7_transform.field import HL7Field


class HL7Operation:
    """
    Field operation interface, must be implemented in a child class.
    """
    def __init__(self, source_fields, args):
        raise NotImplementedError()

    def execute(self, message):
        """
        Executes the operation.
        """
        raise NotImplementedError()

    def __repr__(self):
        return self.__class__.__name__

    @staticmethod
    def from_name(name, *args):
        """Creates the proper operation class instance by name"""
        operations = {
            'copy_value':           CopyValueOperation,
            'add_values':           AddValuesOperation,
            'set_value':            SetValueOperation,
            'concatenate_values':   ConcatenateOperation,
            }
        return operations[name](*args)


class AddValuesOperation(HL7Operation):
    """
    Sums up a list of field values to one value
    using type conversion as given by `args.type`.
    """
    def __init__(self, source_fields, args):
        """
        source_fields ordered list of fields from where the values will be read
        args encodes the target type of field values. Currently supported are:
            int, float, str (default).
        """
        self.source_fields = [HL7Field(field) for field in source_fields]
        if args['type'] == 'int':
            self.convert_to_type = int
        elif args['type'] == 'float':
            self.convert_to_type = float
        else:
            self.convert_to_type = str

    def execute(self, message):
        return str(sum(self.convert_to_type(message[field]) for field in self.source_fields))


class CopyValueOperation(HL7Operation):
    def __init__(self, source_fields, args):
        if len(source_fields) != 1:
            raise RuntimeError("CopyValueOperation can only copy one field value.")
        self.field = HL7Field(source_fields[0])

    def execute(self, message):
        return message[self.field]


class SetValueOperation(HL7Operation):
    def __init__(self, source_fields, args):
        self.value = args['value']

    def execute(self, message):
        return self.value


class ConcatenateOperation(HL7Operation):
    def __init__(self, source_fields, args):
        self.fields = [HL7Field(field) for field in source_fields]
        self.separator = args['separator']

    def execute(self, message):
        return self.separator.join(message[field] for field in self.fields)
