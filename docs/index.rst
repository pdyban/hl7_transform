hl7_transform
=============

hl7_transform is a tool to modify and transform HL7 messages using a mapping scheme.
It can be used as a standalone tool or as a Python library.

How to use
----------
Install hl7_transform from Pypi::

    pip install hl7_transform

Once installed, you can run hl7_transform script in your shell::

    hl7_transform --help

You can also build your own projects or experiment in Jupyter notebooks
by importing the library in your Python code::

    from hl7_transform.mapping import HL7Mapping
    from hl7_transform.transform import HL7Transform
    from hl7_transform.message import HL7Message

    mapping = HL7Mapping.from_json('hl7_transform/test/test_transform.json')
    message = HL7Message.from_file('hl7_transform/test/test_msg.hl7')
    transform = HL7Transform(mapping)
    transformed_message = transform.execute(message)

Features
--------

- read an HL7 message from file, transform it and write it to a new file

Contribute
----------

This project strives from contribution, you are very welcome to
extend functionality and make pull request. The easiest ways to contribute are:

- extend list of operations (see hl7_transform.operations module)
- check issue tracker: `github.com/pdyban/hl7_transform/issues`_
- improve source code: `github.com/pdyban/hl7_transform`_

.. _`github.com/pdyban/hl7_transform/issues`: https://github.com/pdyban/hl7_transform/issues
.. _`github.com/pdyban/hl7_transform`: https://github.com/pdyban/hl7_transform

If you are having issues, please let us know.

API Documentation
-----------------

.. toctree::
   :maxdepth: 2

   mapping
   message
   operations
   transform

License
-------

The project is licensed under the MIT license.
