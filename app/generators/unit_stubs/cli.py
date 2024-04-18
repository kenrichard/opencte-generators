from .outline import generate_outline


def create_outline_subparser(subparsers):
    parser = subparsers.add_parser("outline")
    parser.add_argument("--debug")
    parser.add_argument("--course_key", type=str, required=True)


def process_outline(args):
    course_key = args.course_key
    generate_outline(course_key)
