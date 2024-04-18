from .pages import generate_all_pages, generate_pages


def create_pages_subparser(subparsers):
    parser = subparsers.add_parser("pages", help="Generate Lesson")
    parser.add_argument("--debug")
    parser.add_argument("--course_key", type=str, required=True)
    parser.add_argument("--unit_key", type=str, required=True)
    parser.add_argument("--lesson_key", type=str)


def process_pages(args):
    """Function processing CLI commands for lesson"""
    course_key = args.course_key
    unit_key = args.unit_key

    if args.lesson_key is None:
        generate_all_pages(course_key, unit_key)
    else:
        generate_pages(course_key, unit_key, args.lesson_key)
