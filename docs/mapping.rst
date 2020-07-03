Mapping rules
=============

Messages can be transformed using a mapping scheme. This page describes
how such a mapping scheme is constructed.

An HL7 message consists of a list of segments, each of them in turn containing fields.
The mapping scheme defines how fields of the given message have to be transformed.

If we take an example message::

    MSH|^~\&|Doctolib||Doctolib||20200522153917||SIU^S12|d051c31adcc460b5289f|P|2.5.1|||||FRA|UTF-8
    SCH||8678012^Doctolib||||neu_pat^Neupatient|||||^^20^202005201615|||||111683^Jackson^Heights||||Doctolib|||||Booked
    NTE|||Some notes
    PID|||19619205^^^Doctolib^PI||Test^Otto^^^^^L||19900101|M|Geburtsname^^^^^^M||Wilhelmstrasse 118^^Berlin^^11111||+491738599814^^^jackson.heights@doctolib.com~+49301234567
    RGS|1
    AIG|1|||allg_chir^Allg. Chirurgie

and an example mapping scheme in JSON format::

    [
      {
          "target_field": "TQ1.7",
          "operation": "copy_value",
          "source_field": "SCH.11.4"
      }
    ]

Then the resulting message will contain all fields of the source message, plus
a new TQ1 segment with the value from field SCH.11.4 copied into field TQ1.7::

    MSH|^~\&|Doctolib||Doctolib||20200522153917||SIU^S12|d051c31adcc460b5289f|P|2.5.1|||||FRA|UTF-8
    SCH||8678012^Doctolib||||neu_pat^Neupatient|||||^^20^202005201615|||||111683^Jackson^Heights||||Doctolib|||||Booked
    NTE|||Some notes
    PID|||19619205^^^Doctolib^PI||Test^Otto^^^^^L||19900101|M|Geburtsname^^^^^^M||Wilhelmstrasse 118^^Berlin^^11111||+491738599814^^^jackson.heights@doctolib.com~+49301234567
    RGS|1
    AIG|1|||allg_chir^Allg. Chirurgie
    TQ1|||||||202005201615

Mapping scheme file
-------------------

A mapping scheme can be represented either in JSON or in CSV format.
CSV format does not support all operations.

JSON-formatted mapping scheme file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An example JSON mapping scheme::

    [
      {"target_field": "PID.3", "operation": "set_value", "args": {"value": "123^PatID"}},
      {"target_field": "PV1.2", "operation": "copy_value", "source_field": "PID.18"},
      {"target_field": "PV1.10", "operation": "set_value", "args": {"value": "1922"}}
    ]

CSV-formatted mapping scheme file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An example CSV mapping scheme is an equivalent to the JSON mapping scheme above:

============  ==========  ============  ==========
target_field  operation   source_field  args.value
============  ==========  ============  ==========
PID.3         set_value                 123^PatID
PV1.2         copy_value  PID.18
PV1.10        set_value   1922
============  ==========  ============  ==========

Operations
----------
A mapping scheme consists of a list of operations, e.g.::

    [
      {
        "target_field": "MSH.9.2",
        "operation": "set_value",
        "args": {"value": "S12"}
      },
      {
        "target_field": "MSH.9.3",
        "operation": "set_value",
        "args": {"value": "SIU_S12"}
      }
    ]

This mapping consists of two operations, both of type "set_value". The full list of supported operations can be found in :ref:`List of supported operations`.

Every operation consists of a number of mandatory fields: "target_field",
"operation" and "args".

    ``target_field`` defines the field where the value shall be written into
    ``operation`` define the operation type (e.g. copy, add etc.)
    ``args`` is a dictionary of optional arguments that depend on the operation.

List of supported operations
----------------------------

  .. automodule:: hl7_transform.operations
    :members:
