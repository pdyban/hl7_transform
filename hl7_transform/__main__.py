"""
This package allows transformation of HL7 messages using field mapping.

\author Pavlo Dyban (Doctolib GmbH)
\date   26-May-2020
"""

import argparse
from .cli import main_cli


def main():
    parser = argparse.ArgumentParser(
            description="""Transform HL7 messages using a mapping scheme.""")
    parser.add_argument('message',
            help="path to the HL7 message file, e.g. siu_s12_in.hl7")
    parser.add_argument('mappingfile',
            help='path to file containing field mapping, e.g. mapping.json',
            type=str)
    parser.add_argument('outfile',
            help="path to the output HL7 message file, e.g. siu_s12_out.hl7")
    parser.add_argument('--type',
            help='mapping file type, can be json (default) or csv',
            default='json',
            type=str)

    args = parser.parse_args()
    main_cli(args)


if __name__ == '__main__':
    main()
