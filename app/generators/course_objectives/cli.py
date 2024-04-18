from course_objectives import course_objectives


def create_course_objectives_subparser(subparsers):
    parser = subparsers.add_parser("course-objectives")
    parser.add_argument("--debug")
    parser.add_argument("--course_key", type=str, required=True)


def process_course_objectives(args):
    course_key = args.course_key
    course_objectives(course_key)
