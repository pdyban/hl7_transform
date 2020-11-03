"""
This package allows transformation of HL7 messages using field mapping.

\author Pavlo Dyban (Doctolib GmbH)
\date   26-May-2020
"""

import argparse
from hl7_transform.mapping import HL7Mapping
from hl7_transform.transform import HL7Transform
from hl7_transform.message import HL7Message


def main_cli(args):
    if args.type == 'json':
        mapping = HL7Mapping.from_json(args.mappingfile)
    elif args.type == 'csv':
        mapping = HL7Mapping.from_csv(args.mappingfile)
    else:
        raise ArgumentError('Unsupported mapping file type. Currently supported are: json, csv.')
    transform = HL7Transform(mapping)
    if args.message:
        message = HL7Message.from_file(args.message)
    else:
        message = HL7Message.new()
    message_transformed = transform(message)
    if args.out is not None:
        with open(args.out, 'w') as f_out:
            f_out.write(message_transformed.to_string())
    else:
        print(message_transformed.to_string())

def main():
    parser = argparse.ArgumentParser(
            description="""Transform HL7 messages using a mapping scheme.""")
    parser.add_argument('mappingfile',
            help='path to file containing field mapping, e.g. mapping.json',
            type=str)
    parser.add_argument('-m', '--message',
            help="path to the HL7 message file, e.g. siu_s12_in.hl7")
    parser.add_argument('-o', '--out',
            help="path to the output HL7 message file, e.g. siu_s12_out.hl7")
    parser.add_argument('--type',
            help='mapping file type, can be json (default) or csv',
            default='json',
            type=str)

    args = parser.parse_args()
    main_cli(args)


if __name__ == '__main__':
    main()
