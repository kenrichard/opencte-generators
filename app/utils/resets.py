from app.models.standards import delete_standards
from app.models.lessons import delete_course_lessons, delete_unit_lessons
from app.models.units import delete_units


def reset_course(course_key):
    delete_course_lessons(course_key)
    delete_units(course_key)
    delete_standards(course_key)


def reset_outline(course_key):
    delete_course_lessons(course_key)
    delete_units(course_key)


def reset_lessons(course_key, unit_key):
    delete_unit_lessons(course_key, unit_key)
