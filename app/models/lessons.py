""" Data Model - Lesson (Units have a set of Lessons) """

import json
import os
import datetime
from typing import Optional
import psycopg2
from pydantic import BaseModel
from app.models.course import load_course
from app.utils.db_dynamo import (
    DynamoBase,
    dynamo_load,
    dynamo_prefix_delete,
    dynamo_prefix_query,
    dynamo_save,
)
from app.models.units import UnitStandard, load_unit

##
## LESSONS
##

LESSON_SK_PREFIX = "LESSON~"


class LessonPage(BaseModel):
    """Lesson Data - Page"""

    page_number: int
    page_heading: str
    page_content: list[str]
    page_heading_es: Optional[str] = None
    page_content_es: Optional[list[str | None]] = None


class LessonQuestionChoice(BaseModel):
    """Lesson Data - Question Choice"""

    choice: str
    correct: str


class LessonQuestion(BaseModel):
    """Lesson Data - Question"""

    question_number: int
    question_text: str
    quiz_choices: list[LessonQuestionChoice]


class LessonVocab(BaseModel):
    """Lesson Data - Vocab"""

    word: str
    definition: str
    word_es: str
    definition_es: str


class Lesson(DynamoBase):
    """Lesson Data Model"""

    course_key: str
    unit_key: str
    lesson_key: str
    title: str
    summary: Optional[str] = None
    keywords: Optional[list[str]] = None
    topics: Optional[list[str]] = None
    concepts: Optional[list[str]] = None
    skills: Optional[list[str]] = None
    procedures: Optional[list[str]] = None
    standards: Optional[list[UnitStandard]] = None
    pages: Optional[list[LessonPage]] = None
    quiz_questions: Optional[list[LessonQuestion]] = None
    vocab: Optional[list[LessonVocab]] = None
    seq: int
    prompt_pages: Optional[bool] = None
    prompt_quiz: Optional[bool] = None
    rebuild_lesson: Optional[bool] = False
    retranslate_lesson: Optional[bool] = False
    embeddings_summary: Optional[str] = None
    embeddings_keywords: Optional[str] = None
    embeddings_text: Optional[str] = None
    google_slides_id: Optional[str] = None
    course_title: str
    unit_title: str
    ts: Optional[str] = None


def lesson_pk(course_key: str):
    return "COURSE~" + course_key


def lesson_sk(unit_key: str, lesson_key: str):
    return LESSON_SK_PREFIX + unit_key + "~" + lesson_key


def save_lesson(lesson: Lesson):
    lesson.pk = lesson_pk(lesson.course_key)
    lesson.sk = lesson_sk(lesson.unit_key, lesson.lesson_key)
    lesson.ts = datetime.datetime.now().astimezone().isoformat()
    dynamo_save(lesson)


def load_lesson(course_key: str, unit_key: str, lesson_key):
    data = dynamo_load(lesson_pk(course_key), lesson_sk(unit_key, lesson_key))
    return Lesson(**data)


def load_lessons(course_key, unit_key):
    data = dynamo_prefix_query(lesson_pk(course_key), lesson_sk(unit_key, ""))
    return [Lesson(**row) for row in data]


def delete_unit_lessons(course_key, unit_key):
    dynamo_prefix_delete(lesson_pk(course_key), lesson_sk(unit_key, ""))


def delete_course_lessons(course_key):
    dynamo_prefix_delete(lesson_pk(course_key), LESSON_SK_PREFIX)


def save_new_lessons(course_key, unit_key, response):
    for index, row in enumerate(response["lessons"]):
        lesson_key = "L%03d" % (index + 1,)
        print("Saving Lesson for " + course_key + " " + unit_key + " " + lesson_key)

        title = row["title"]
        topics = row["topics"]
        concepts = row["concepts"]
        skills = row["skills"]
        procedures = row["procedures"]
        standards = row["standards"]

        course = load_course(course_key)
        unit = load_unit(course_key, unit_key)

        lesson = Lesson(
            course_key=course_key,
            unit_key=unit_key,
            lesson_key=lesson_key,
            title=title,
            topics=topics,
            concepts=concepts,
            skills=skills,
            procedures=procedures,
            standards=standards,
            course_title=course.title,
            unit_title=unit.title,
            seq=index,
            ts=datetime.datetime.now().astimezone().isoformat(),
        )
        save_lesson(lesson)


def save_lesson_pages(
    course_key,
    unit_key,
    lesson_key,
    pages,
):
    lesson = load_lesson(course_key, unit_key, lesson_key)
    lesson.pages = [LessonPage(**row) for row in pages]
    lesson.rebuild_lesson = None
    lesson.retranslate_lesson = True

    # Reset other fields for future passes
    lesson.google_slides_id = None
    lesson.embeddings_text = None
    lesson.embeddings_keywords = None
    lesson.embeddings_summary = None
    lesson.retranslate_lesson = None
    lesson.summary = None
    lesson.ts = (datetime.datetime.now().astimezone().isoformat(),)

    save_lesson(lesson)


def save_lesson_quiz(
    course_key,
    unit_key,
    lesson_key,
    quiz,
):
    # Quiz First - Reset Other Lesson Fields
    lesson = load_lesson(course_key, unit_key, lesson_key)
    lesson.rebuild_lesson = None
    lesson.retranslate_lesson = True
    lesson.google_slides_id = None
    lesson.embeddings_text = None
    lesson.embeddings_keywords = None
    lesson.embeddings_summary = None
    lesson.retranslate_lesson = None
    lesson.summary = None
    lesson.pages = None
    lesson.vocab = None
    lesson.quiz_questions = [LessonQuestion(**row) for row in quiz]
    lesson.ts = (datetime.datetime.now().astimezone().isoformat(),)
    save_lesson(lesson)


def save_lesson_postgres(lesson: Lesson):
    unit = load_unit(lesson.course_key, lesson.unit_key)
    course = load_course(lesson.course_key)
    connection = psycopg2.connect(os.environ["POSTGRES_URL"])

    # First, delete existing data matching the keys
    delete_sql = """
        DELETE FROM lessons
        WHERE course_key = %s AND unit_key = %s AND lesson_key = %s
    """

    # Convert optional fields and lists to JSON
    topics_json = json.dumps(lesson.topics) if lesson.topics is not None else None
    concepts_json = json.dumps(lesson.concepts) if lesson.concepts is not None else None
    skills_json = json.dumps(lesson.skills) if lesson.skills is not None else None
    procedures_json = (
        json.dumps(lesson.procedures) if lesson.procedures is not None else None
    )

    # Prepare the SQL insert statement
    sql = """
    INSERT INTO lessons (
        course_key, unit_key, lesson_key, title, summary,
        topics, concepts, skills, procedures,
        unit_title, course_title, course_theme, course_publisher,
        embeddings_summary, embeddings_keywords, embeddings_text
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    keys_data = (lesson.course_key, lesson.unit_key, lesson.lesson_key)
    insert_data = (
        lesson.course_key,
        lesson.unit_key,
        lesson.lesson_key,
        lesson.title,
        lesson.summary,
        topics_json,
        concepts_json,
        skills_json,
        procedures_json,
        unit.title,
        course.title,
        course.theme,
        course.publisher,
        lesson.embeddings_summary,
        lesson.embeddings_keywords,
        lesson.embeddings_text,
    )

    # Execute the SQL command
    with connection.cursor() as cursor:
        cursor.execute(delete_sql, keys_data)
        cursor.execute(sql, insert_data)
        connection.commit()


def lesson_search_summary(embeddings, max_results=3, min_threshold=0.7):
    connection = psycopg2.connect(os.environ["POSTGRES_URL"])

    query = """
    SELECT
        course_key, unit_key, lesson_key, title, summary,
        topics, concepts, skills, procedures,
        unit_title, course_title, course_theme, course_publisher,
        1 - (embeddings_summary <=> %s) as score
    FROM
        lessons
    WHERE
        1 - (embeddings_summary <=> %s) > %s
    ORDER BY
        embeddings_summary <=> %s LIMIT %s
    """
    embeddings_param = "[" + ",".join(map(str, embeddings)) + "]"
    params = [
        embeddings_param,
        embeddings_param,
        min_threshold,
        embeddings_param,
        max_results,
    ]

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows


def lesson_search_keywords(embeddings, max_results=3, min_threshold=0.7):
    connection = psycopg2.connect(os.environ["POSTGRES_URL"])

    query = """
    SELECT
        course_key, unit_key, lesson_key, title, summary,
        topics, concepts, skills, procedures,
        unit_title, course_title, course_theme, course_publisher,
        1 - (embeddings_keywords <=> %s) as score
    FROM
        lessons
    WHERE
        1 - (embeddings_keywords <=> %s) > %s
    ORDER BY
        embeddings_keywords <=> %s LIMIT %s
    """
    embeddings_param = "[" + ",".join(map(str, embeddings)) + "]"
    params = [
        embeddings_param,
        embeddings_param,
        min_threshold,
        embeddings_param,
        max_results,
    ]

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows


def lesson_search_pages(embeddings, max_results=3, min_threshold=0.7):
    connection = psycopg2.connect(os.environ["POSTGRES_URL"])

    query = """
    SELECT
        course_key, unit_key, lesson_key, title, summary,
        topics, concepts, skills, procedures,
        unit_title, course_title, course_theme, course_publisher,
        1 - (embeddings_text <=> %s) as score
    FROM
        lessons
    WHERE
        1 - (embeddings_text <=> %s) > %s
    ORDER BY
        embeddings_text <=> %s LIMIT %s
    """
    embeddings_param = "[" + ",".join(map(str, embeddings)) + "]"
    params = [
        embeddings_param,
        embeddings_param,
        min_threshold,
        embeddings_param,
        max_results,
    ]

    with connection.cursor() as cursor:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return rows
