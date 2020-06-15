# Introduction

``hl7_transform`` is a Python package that allows for transformation of HL7 messages
using a field mapping dictionary.

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
