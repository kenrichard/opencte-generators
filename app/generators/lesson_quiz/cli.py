from app.generators.lesson_quiz.quiz import generate_quiz


def create_quiz_subparser(subparsers):
    parser = subparsers.add_parser("quiz")
    parser.add_argument("--debug")
    parser.add_argument("--course_key", type=str, required=True)
    parser.add_argument("--unit_key", type=str, required=True)
    parser.add_argument("--lesson_key", type=str)


def process_quiz(args):
    course_key = args.course_key
    unit_key = args.unit_key
    lesson_key = args.lesson_key
    generate_quiz(course_key, unit_key, lesson_key)
