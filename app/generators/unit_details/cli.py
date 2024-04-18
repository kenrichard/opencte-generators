from .unit import expand_unit


def create_unit_subparser(subparsers):
    parser = subparsers.add_parser("unit")
    parser.add_argument("--debug")
    parser.add_argument("--course_key", type=str, required=True)
    parser.add_argument("--unit_key", type=str, required=True)


def process_unit(args):
    course_key = args.course_key
    unit_key = args.unit_key
    expand_unit(course_key, unit_key)
