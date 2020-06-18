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
    message = HL7Message.from_file(args.message)
    message_transformed = transform.execute(message)
    with open(args.outfile, 'w') as f_out:
        f_out.write(message_transformed.to_string())
