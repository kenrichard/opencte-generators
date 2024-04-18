from app.utils.cli import validate_file
from .ingest import ingest


def create_ingest_subparser(subparsers):
    parser = subparsers.add_parser("ingest", help="ingest Standards")
    parser.add_argument("--debug")
    parser.add_argument("--input", type=validate_file, required=True)
    parser.add_argument("--course_key", type=str, required=True)
    parser.add_argument("--course_id", type=str, required=True)
    parser.add_argument("--course_title", type=str, required=True)
    parser.add_argument("--publisher", type=str, required=True)
    parser.add_argument("--grade", type=str, required=True)
    parser.add_argument("--theme", type=str, required=True)
    parser.add_argument("--unit_count", type=int, required=True)


def process_ingest(args):
    course_key = args.course_key
    course_id = args.course_id
    course_title = args.course_title
    publisher = args.publisher
    grade = args.grade
    theme = args.theme
    unit_count = args.unit_count

    # Read Input File
    with open(args.input, "r", encoding="utf-8") as file:
        data = file.read()

    ingest(
        data=data,
        course_key=course_key,
        course_id=course_id,
        course_title=course_title,
        publisher=publisher,
        grade=grade,
        theme=theme,
        unit_count=unit_count,
    )
