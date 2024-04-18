from index_lesson import index_lesson


def create_index_lesson_subparser(subparsers):
    parser = subparsers.add_parser("index")
    parser.add_argument("--debug")
    parser.add_argument("--course_key", type=str, required=True)
    parser.add_argument("--unit_key", type=str, required=True)
    parser.add_argument("--lesson_key", type=str, required=True)


def process_index_lesson(args):
    course_key = args.course_key
    unit_key = args.unit_key
    lesson_key = args.lesson_key
    index_lesson(course_key, unit_key, lesson_key)
