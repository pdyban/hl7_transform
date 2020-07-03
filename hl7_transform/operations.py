"""
Operations on HL7 fields.
"""

from hl7_transform.field import HL7Field
import hashlib
import random
from datetime import datetime


class HL7Operation:
    """
    An Operation interface, all operations must derive from this class.
    """
    def __init__(self, source_fields, args):
        raise NotImplementedError()

    def execute(self, message):
        """Applies the operation to the message"""
        raise NotImplementedError()

    def __repr__(self):
        return self.__class__.__name__

    @staticmethod
    def from_name(name, *args):
        """
        Creates the proper operation class instance by name.

        :param name: The name of the operation. Currently available operations are:
            - copy_value:                   :class:`CopyValueOperation`,
            - add_values:                   AddValuesOperation,
            - set_value:                    SetValueOperation,
            - concatenate_values:           ConcatenateOperation,
            - generate_alphanumeric_id:     GenerateAplhanumericID,
            - generate_numeric_id:          GenerateNumericID,
            - generate_current_datetime:    GenerateCurrentDatetime,
            - set_end_time:                 SetEndTime

        """
        operations = {
            'copy_value':                   CopyValueOperation,
            'add_values':                   AddValuesOperation,
            'set_value':                    SetValueOperation,
            'concatenate_values':           ConcatenateOperation,
            'generate_alphanumeric_id':     GenerateAplhanumericID,
            'generate_numeric_id':          GenerateNumericID,
            'generate_current_datetime':    GenerateCurrentDatetime,
            'set_end_time':                 SetEndTime,
            }
        try:
            return operations[name](*args)
        except KeyError as e:
            raise KeyError("{} is not a valid operation name. Available operations are: {}".format(name, ', '.join(operations.keys())))


class AddValuesOperation(HL7Operation):
    """
    Sums up a list of field values to one value
    using type conversion as given by `args.type`.

    Example usage in a mapping scheme::

        [
            {
                "target_field": "TQ1.8",
                "operation": "add_values",
                "source_fields": ["SCH.11.4", "SCH.11.3"],
                "args": {"type": "int"}
            }
        ]
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
    """
    Copies a value from one field to the other.

    Example usage in a mapping scheme::

        [
            {
                "target_field": "TQ1.9",
                "operation": "copy_value",
                "source_field": "SCH.11.3"
            }
        ]
    """
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


class GenerateAplhanumericID(SetValueOperation):
    """
    Generates an alphanumeric ID, producing a random string encoded in the
    hexadecimal system of length 32 bytes.
    This is useful for creating random message identifiers.
    """
    def __init__(self, source_fields, args):
        args['value'] = hashlib.md5(str(random.random()).encode()).hexdigest()
        SetValueOperation.__init__(self, source_fields, args)


class GenerateNumericID(SetValueOperation):
    """
    Generates an numeric ID, producing a random string encoded with digits
    in decimal system of length 9 digits.
    This is useful for creating random patient or event identifiers.
    """
    def __init__(self, source_fields, args):
        args['value'] = '{:09}'.format(random.randint(0,1e9))
        SetValueOperation.__init__(self, source_fields, args)


class GenerateCurrentDatetime(SetValueOperation):
    """
    Generates current datetime as a string in HL7 format.
    This is useful for creating event timestamps.
    """
    def __init__(self, source_fields, args):
        args['value'] = datetime.now().strftime('%Y%m%d%H%M%S')
        SetValueOperation.__init__(self, source_fields, args)


class ConcatenateOperation(HL7Operation):
    def __init__(self, source_fields, args):
        self.fields = [HL7Field(field) for field in source_fields]
        self.separator = args['separator']

    def execute(self, message):
        return self.separator.join(message[field] for field in self.fields)


class SetEndTime(HL7Operation):
    """Computes end time based on start time and duration."""
    def __init__(self, source_fields, args):
        self.dt = HL7Field(source_fields[0])
        self.duration = HL7Field(source_fields[1])

    def execute(self, message):
        dt = message[self.dt]
        duration = message[self.duration]
        return str(int(dt) + int(duration)*(10**(len(dt) - 12)))
