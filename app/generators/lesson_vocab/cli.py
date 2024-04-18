from app.generators.lesson_vocab.vocab import generate_vocab


def create_vocab_subparser(subparsers):
    parser = subparsers.add_parser("vocab")
    parser.add_argument("--debug")
    parser.add_argument("--course_key", type=str, required=True)
    parser.add_argument("--unit_key", type=str, required=True)
    parser.add_argument("--lesson_key", type=str)


def process_vocab(args):
    course_key = args.course_key
    unit_key = args.unit_key
    lesson_key = args.lesson_key
    generate_vocab(course_key, unit_key, lesson_key)
