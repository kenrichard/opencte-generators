from app.models.lessons import load_lesson
from .translate import translate_lesson, translate_text


def create_translate_subparser(subparsers):
    parser = subparsers.add_parser("translate")
    parser.add_argument("--debug")
    parser.add_argument("--course_key", type=str, required=True)
    parser.add_argument("--unit_key", type=str, required=True)
    parser.add_argument("--lesson_key", type=str, required=True)


def process_translate(args):
    """Function processing CLI commands for lesson"""
    course_key = args.course_key
    unit_key = args.unit_key
    lesson_key = args.lesson_key
    lesson = load_lesson(course_key, unit_key, lesson_key)
    translate_lesson(lesson)
