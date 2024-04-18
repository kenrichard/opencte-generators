import argparse
import logging
from app.generators.course_themes.cli import (
    create_course_themes_subparser,
    process_course_themes,
)
from app.generators.lesson_export_google_sheets.cli import (
    create_google_sheets_subparser,
    process_google_sheets,
)
from app.generators.lesson_index.cli import (
    create_index_lesson_subparser,
    process_index_lesson,
)
from app.generators.course_ingest.cli import create_ingest_subparser, process_ingest
from app.generators.lesson_quiz.cli import create_quiz_subparser, process_quiz
from app.generators.lesson_vocab.cli import create_vocab_subparser, process_vocab
from app.generators.course_objectives.cli import (
    create_course_objectives_subparser,
    process_course_objectives,
)
from app.generators.unit_stubs.cli import create_outline_subparser, process_outline
from app.generators.reset.cli import create_reset_subparser, process_reset
from app.generators.pages_translate.cli import (
    create_translate_subparser,
    process_translate,
)
from app.generators.unit_details.cli import create_unit_subparser, process_unit
from app.generators.lessons_generate.cli import (
    create_lessons_subparser,
    process_lessons,
)
from app.generators.pages_generate.cli import create_pages_subparser, process_pages
from app.generators.queue.cli import create_queue_subparser, process_queue


def create_parsers():
    parser = argparse.ArgumentParser(description="CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    create_course_objectives_subparser(subparsers)
    create_course_themes_subparser(subparsers)
    create_google_sheets_subparser(subparsers)
    create_index_lesson_subparser(subparsers)
    create_ingest_subparser(subparsers)
    create_lessons_subparser(subparsers)
    create_outline_subparser(subparsers)
    create_pages_subparser(subparsers)
    create_queue_subparser(subparsers)
    create_quiz_subparser(subparsers)
    create_reset_subparser(subparsers)
    create_translate_subparser(subparsers)
    create_unit_subparser(subparsers)
    create_vocab_subparser(subparsers)
    return parser


def process_command(args):
    if args.command == "ingest":
        process_ingest(args)
    elif args.command == "outline":
        process_outline(args)
    elif args.command == "unit":
        process_unit(args)
    elif args.command == "lessons":
        process_lessons(args)
    elif args.command == "pages":
        process_pages(args)
    elif args.command == "queue":
        process_queue(args)
    elif args.command == "reset":
        process_reset()
    elif args.command == "translate":
        process_translate(args)
    elif args.command == "index":
        process_index_lesson(args)
    elif args.command == "sheets":
        process_google_sheets(args)
    elif args.command == "course-objectives":
        process_course_objectives(args)
    elif args.command == "process_vocab":
        process_vocab(args)
    elif args.command == "quiz":
        process_quiz(args)
    elif args.command == "course-themes":
        process_course_themes(args)
    else:
        print("Command not found")


def setup_cli():
    parser = create_parsers()
    args = parser.parse_args()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    process_command(args)
