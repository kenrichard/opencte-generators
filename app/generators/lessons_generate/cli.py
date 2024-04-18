from .lessons import generate_lessons


def create_lessons_subparser(subparsers):
    parser = subparsers.add_parser("lessons")
    parser.add_argument("--debug")
    parser.add_argument("--course_key", type=str, required=True)
    parser.add_argument("--unit_key", type=str, required=True)


def process_lessons(args):
    course_key = args.course_key
    unit_key = args.unit_key
    generate_lessons(course_key, unit_key)
