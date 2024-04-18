import logging
from app.models.course import load_course
from app.models.lessons import load_lesson, load_lessons, save_lesson_pages
from app.utils.flatten import (
    list_to_text,
    quiz_questions_to_text,
    unit_standards_to_text,
    vocab_to_text,
)
from app.utils.chatgpt import open_ai_submit_json
from app.models.units import load_unit
from .prompt import prompt_lesson_pages_v2

READING_LEVEL = "8th"


def generate_pages(course_key, unit_key, lesson_key):
    keys = {
        "course_key": course_key,
        "unit_key": unit_key,
        "lesson_key": lesson_key,
    }

    course = load_course(course_key)
    unit = load_unit(course_key, unit_key)
    lesson = load_lesson(course_key, unit_key, lesson_key)
    grade_level = READING_LEVEL  # course.grade
    theme = course.theme

    print(
        f"Generating Pages (Step 1): {course_key}~{unit_key}~{lesson_key} Theme={theme} Grade={grade_level}"
    )

    unit_title = unit.title

    logging.debug(lesson.concepts)

    lesson_title = lesson.title
    topics = "\n".join(lesson.topics)
    concepts = "\n".join(lesson.concepts)
    skills = "\n".join(lesson.skills)
    procedures = "\n".join(lesson.procedures)
    standards = "\n".join(map(lambda x: x.standard, lesson.standards))
    quiz = quiz_questions_to_text(lesson.quiz_questions)
    vocab = vocab_to_text(lesson.vocab)

    page_prompt = prompt_lesson_pages_v2(
        grade_level=grade_level,
        theme=theme,
        unit_title=unit_title,
        lesson_title=lesson_title,
        topics=topics,
        concepts=concepts,
        skills=skills,
        procedures=procedures,
        standards=standards,
        quiz=quiz,
        vocab=vocab,
    )
    # print(page_prompt)

    lesson.prompt_pages = page_prompt
    page_results = open_ai_submit_json(page_prompt, "Create Lesson Pages", keys)

    save_lesson_pages(
        course_key,
        unit_key,
        lesson_key,
        page_results["pages"],
    )


def generate_all_pages(course_key, unit_key):
    lessons = load_lessons(course_key, unit_key)
    for lesson in lessons:
        generate_pages(course_key, unit_key, lesson.lesson_key)
