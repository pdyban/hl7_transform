"""
This package allows transformation of HL7 messages using field mapping.

\author Pavlo Dyban (Doctolib GmbH)
\date   26-May-2020
"""

import argparse

def main():
    parser = argparse.ArgumentParser(
            description="""Transform HL7 messages.""")
    parser.add_argument('infile',
            help="path to the HL7 message file, e.g. siu_s12_in.hl7")
    parser.add_argument('outfile',
            help="path to the output HL7 message file, e.g. siu_s12_out.hl7")
    parser.add_argument('mappingfile',
            help='JSON file containing field mapping',
            type=str)
    parser.add_argument('--encoding',
            help='encoding of the log file, e.g. latin1',
            type=str,
            default='utf-8')

    args = parser.parse_args()


if __name__ == '__main__':
    main()
