from app.generators.lessons_generate.lessons import generate_lessons
from app.generators.unit_stubs.outline import generate_outline
from app.generators.pages_generate.pages import generate_pages
from app.generators.unit_details.unit import expand_unit
from app.models.course import load_all_courses
from app.models.lessons import load_lessons, save_lesson
from app.models.units import load_units

##
## Marks Lessons for Rebuild
##


def create_reset_subparser(subparsers):
    parser = subparsers.add_parser("reset")
    parser.add_argument("--debug")


def process_reset():
    check_courses()


def check_courses():
    courses = load_all_courses()
    for course in courses:
        units = load_units(course.course_key)
        if len(units) != 0:
            for unit in units:
                check_unit(unit)


def check_unit(unit):
    if unit.summary is None:
        return
    lessons = load_lessons(unit.course_key, unit.unit_key)
    if len(lessons) != 0:
        for lesson in lessons:
            check_lesson(lesson)


def check_lesson(lesson):
    if lesson.pages is not None:
        print(
            "Marking For Reset: "
            + lesson.course_key
            + " "
            + lesson.unit_key
            + " "
            + lesson.lesson_key
        )
        lesson.rebuild_lesson = True
        lesson.page_content_es = None
        lesson.page_heading_es = None
        save_lesson(lesson)
