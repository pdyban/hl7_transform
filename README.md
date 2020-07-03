# Introduction

``hl7_transform`` is a Python package that allows for transformation of HL7 messages
using a field mapping dictionary.

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity) ![Docs build status](https://readthedocs.org/projects/hl7-transform/badge/?version=latest) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/pdyban/hl7_transform/CI) [![PyPI license](https://img.shields.io/pypi/l/hl7-transform.svg)](https://pypi.python.org/pypi/hl7-transform/) [![PyPI pyversions](https://img.shields.io/pypi/pyversions/hl7-transform.svg)](https://pypi.python.org/pypi/hl7-transform/)

As a standard, HL7 permits different ways of implementing message interfaces
between systems. For example two systems that exchange ADT or SIU messages often
pass the same information in different fields.
In a hospital, an integration engine would map one type of HL7 messages
to another, transforming the messages on the fly as they are passed through
the interfaces.
This Python package allows you to test message transformation without having
an integration engine in place. You can modify your HL7 message structure freely,
by using a JSON-encoded mapping of fields,
then evaluate the conformance of the newly created transformed messages
to the target software.

A live example of this package at work can be found in [hl7_transform_web](https://github.com/pdyban/hl7_transform_web) repository and online.

# How to use

The easiest way to use this library is to install it from Pypi:

```py
pip install hl7_transform
```

Alternatively, you can download and build this package from source:

```bash
git clone https://github.com/pdyban/hl7_transform.git
python setup.py build
python setup.py install
```

After installation, you can use the Python library in your own projects as well as call standalone script hl7_transform in the shell console of your choice.

```bash
hl7_transform --help
```

You can also build your own projects or experiment in Jupyter notebooks by importing the library in your Python code:

```py
from hl7_transform.mapping import HL7Mapping
from hl7_transform.transform import HL7Transform
from hl7_transform.message import HL7Message

mapping = HL7Mapping.from_json('test_transform.json')
message = HL7Message.from_file('test_msg.hl7')
transform = HL7Transform(mapping)
transformed_message = transform.execute(message)
```

For example code, see inside [test](hl7_transform/test) module, in particular [test_transform.py](hl7_transform/test/test_transform.py).

# Documentation

This project is documented using [sphinx](https://www.sphinx-doc.org). The documentation pages can be found in [ReadTheDocs](https://hl7-transform.readthedocs.io/en/latest/).

To understand how the package works, we suggest to start by reading the [Mapping rules](https://hl7-transform.readthedocs.io/en/latest/mapping.html) documentation page.
