from course_themes import course_themes


def create_course_themes_subparser(subparsers):
    parser = subparsers.add_parser("course-themes")
    parser.add_argument("--debug")
    parser.add_argument("--course_key", type=str, required=True)


def process_course_themes(args):
    course_key = args.course_key
    course_themes(course_key)
