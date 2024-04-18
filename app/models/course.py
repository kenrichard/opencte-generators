""" Data Model - Lesson (Course has a set of Units) """

from typing import Optional

from pydantic import BaseModel
from app.utils.db_dynamo import (
    DynamoBase,
    dynamo_load,
    dynamo_prefix_query,
    dynamo_save,
)


class CourseThemes(BaseModel):
    """Course Themes for Course"""

    theme: str
    details: list[str]


class Course(DynamoBase):
    """Course Data Model"""

    course_key: str
    course_id: str
    title: str
    unit_count: Optional[int] = None
    grade: Optional[str] = None
    theme: Optional[str] = None
    publisher: Optional[str] = None
    summary: Optional[str] = None
    themes: Optional[list[CourseThemes]] = None
    status: Optional[str] = None


def course_pk():
    return "COURSE"


def course_sk(course_key: str):
    return "COURSE~" + course_key


def load_all_courses() -> list[Course]:
    data = dynamo_prefix_query(course_pk(), course_sk(""))
    return [Course(**item) for item in data]


def load_course(course_key) -> Course:
    data = dynamo_load(course_pk(), course_sk(course_key))
    return Course(**data)


def save_course(course: Course):
    course.pk = course_pk()
    course.sk = course_sk(course.course_key)
    dynamo_save(course)


def save_new_course(
    course_key, course_id, course_title, publisher, grade, theme, unit_count
):
    course = Course(
        course_key=course_key,
        course_id=course_id,
        title=course_title,
        publisher=publisher,
        grade=grade,
        theme=theme,
        unit_count=unit_count,
    )
    save_course(course)


def update_course_summary(course_key, summary):
    course = load_course(course_key)
    course.summary = summary
    save_course(course)
