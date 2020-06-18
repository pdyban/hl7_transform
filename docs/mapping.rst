Mapping rules
=============

Messages can be transformed using a mapping scheme. This page describes
how such a mapping scheme is structured.

A mapping scheme contains a list of target fields and operations, whose values are written into the target field, e.g.::

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

This library can read mapping schemes from JSON or CSV files.

Example JSON mapping scheme::

    [
      {"target_field": "PID.3", "operation": "set_value", "args": {"value": "123^PatID"}},
      {"target_field": "PV1.2", "operation": "copy_value", "source_field": "PID.18"},
      {"target_field": "PV1.10", "operation": "set_value", "args": {"value": "1922"}}
    ]

Example CSV mapping scheme is an equivalent to the JSON mapping scheme above:

============  ==========  ============  ==========
target_field  operation   source_field  args.value
============  ==========  ============  ==========
PID.3         set_value                 123^PatID
PV1.2         copy_value  PID.18
PV1.10        set_value   1922
============  ==========  ============  ==========

API documentation
-----------------

  .. automodule:: hl7_transform.mapping
    :members:
