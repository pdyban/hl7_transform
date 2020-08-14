"""
A list of operations.
"""

from hl7_transform.field import HL7Field
import hashlib
import random
from datetime import datetime, timedelta


class HL7Operation:
    """
    An Operation interface, all operations must derive from this class.
    """
    def __init__(self, source_fields, args):
        raise NotImplementedError()

    def execute(self, message):
        raise NotImplementedError()

    def __repr__(self):
        return self.__class__.__name__

    @staticmethod
    def from_name(name, *args):
        """
        Creates the proper operation class instance by name.

        :param name: The name of the operation. Currently available operations are:

            - copy_value:                   :class:`CopyValueOperation`,
            - add_values:                   :class:`AddValuesOperation`,
            - set_value:                    :class:`SetValueOperation`,
            - concatenate_values:           :class:`ConcatenateOperation`,
            - generate_alphanumeric_id:     :class:`GenerateAplhanumericID`,
            - generate_numeric_id:          :class:`GenerateNumericID`,
            - generate_current_datetime:    :class:`GenerateCurrentDatetime`,
            - set_end_time:                 :class:`SetEndTime`,

        """
        operations = {
            'copy_value':                   CopyValue,
            'add_values':                   AddValues,
            'set_value':                    SetValue,
            'concatenate_values':           Concatenate,
            'generate_alphanumeric_id':     GenerateAplhanumericID,
            'generate_numeric_id':          GenerateNumericID,
            'generate_current_datetime':    GenerateCurrentDatetime,
            'set_end_time':                 SetEndTime,
            # 'delete_segment':               DeleteSegment,
            }
        try:
            return operations[name](*args)
        except KeyError as e:
            raise KeyError("{} is not a valid operation name. Available operations are: {}".format(name, ', '.join(operations.keys())))


class AddValues(HL7Operation):
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


class CopyValue(HL7Operation):
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


class SetValue(HL7Operation):
    """
    Sets a field to a given value.

    Example usage in a mapping scheme::

        [
            {
                "target_field": "ORC.7.6",
                "operation": "set_value",
                "args": {"value": "6"}
            }
        ]
    """
    def __init__(self, source_fields, args):
        self.value = args['value']

    def execute(self, message):
        return self.value


class GenerateAplhanumericID(SetValue):
    """
    Generates an alphanumeric ID, producing a random string encoded in the
    hexadecimal system of length 32 bytes.
    This is useful for creating random message identifiers.

    Example usage in a mapping scheme::

        [
            {
                "target_field": "MSH.10",
                "operation": "generate_alphanumeric_id"
            }
        ]
    """
    def __init__(self, source_fields, args):
        args['value'] = hashlib.md5(str(random.random()).encode()).hexdigest()
        SetValue.__init__(self, source_fields, args)


class GenerateNumericID(SetValue):
    """
    Generates an numeric ID, producing a random string encoded with digits
    in decimal system of length 9 digits.
    This is useful for creating random patient or event identifiers.

    Example usage in a mapping scheme::

        [
            {
                "target_field": "PID.3.1",
                "operation": "generate_numeric_id"
            }
        ]
    """
    def __init__(self, source_fields, args):
        args['value'] = '{:09}'.format(random.randint(0,1e9))
        SetValue.__init__(self, source_fields, args)


class GenerateCurrentDatetime(SetValue):
    """
    Generates current datetime as a string in HL7 format.
    This is useful for creating event timestamps.

    Example usage in a mapping scheme::

        [
            {
                "target_field": "ORC.9",
                "operation": "generate_current_datetime"
            }
        ]
    """
    def __init__(self, source_fields, args):
        args['value'] = datetime.now().strftime('%Y%m%d%H%M%S')
        SetValue.__init__(self, source_fields, args)


class Concatenate(HL7Operation):
    """
    Concatenates two field values as strings placing a separator in between.

    Example usage in a mapping scheme::

        [
            {
                "target_field": "SCH.9",
                "operation": "concatenate_values",
                "source_fields": ["SCH.11.4", "SCH.11.3"],
                "args": {"separator": " + "}
            }
        ]
    """
    def __init__(self, source_fields, args):
        self.fields = [HL7Field(field) for field in source_fields]
        self.separator = args['separator']

    def execute(self, message):
        return self.separator.join(message[field] for field in self.fields)


class SetEndTime(HL7Operation):
    """Computes end time based on start time and duration.

    Example usage in a mapping scheme::

        [
            {
                "target_field": "SCH.9",
                "operation": "set_end_time",
                "source_fields": ["SCH.11.4", "SCH.11.3"]
            }
        ]
    """
    def __init__(self, source_fields, args):
        self.dt = HL7Field(source_fields[0])
        self.duration = HL7Field(source_fields[1])

    def execute(self, message):
        dt_str = message[self.dt]
        dt_format = ('%Y%m%d%H%M', '%Y%m%d%H%M%S')[len(dt_str) > 12]
        dt = datetime.strptime(dt_str, dt_format)
        duration = timedelta(minutes=int(message[self.duration]))
        end_time = dt + duration
        return end_time.strftime(dt_format)


# class DeleteSegment(HL7Operation):
#     """Deletes a segment given.
#
#     The following operation will remvoe an PID segment from an HL7 message::
#
#     [
#         {
#             "target_field": "PID",
#             "operation": "delete_segment"
#         }
#     ]
#     """
#     def __init__(self, source_fields, args):
#         pass
#
#     def execute(self, message):
#         return None
