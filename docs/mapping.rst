Mapping rules
=============

Messages can be transformed using a mapping scheme. This page describes
how such a mapping scheme is structured.

A mapping scheme is represented by a list of operation items
encoded in JSON format, e.g.::

    [
      {
        "target_field": "MSH.9.3",
        "operation": "set_value",
        "args": {"value": "SIU_S12"}
      }
    ]

This mapping consists of one operation. It sets the value of the
`target_field` to `value`, i.e. field MSH.9.3 is given the string value
of "SIU_S12".

Every operation consists of a number of mandatory fields: "target_field",
"operation" and "args". The content of the "args" dictionary depends
on the definition of the operation and differs from one
operation to the other. For more information, consult the documentation of the operations module.

Mapping files are parsed from JSON files in the following class.

  .. automodule:: hl7_transform.mapping
    :members:
