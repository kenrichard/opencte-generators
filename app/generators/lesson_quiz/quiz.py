from app.generators.pages_generate.pages import READING_LEVEL
from app.models.course import load_course
from app.models.lessons import load_lesson, save_lesson_quiz
from app.utils.chatgpt import open_ai_submit_json
from app.models.units import load_unit
from app.utils.flatten import list_to_text, unit_standards_to_text
from .prompts import prompt_lesson_quiz


def generate_quiz(course_key, unit_key, lesson_key):
    keys = {
        "course_key": course_key,
        "unit_key": unit_key,
        "lesson_key": lesson_key,
    }

    course = load_course(course_key)
    unit = load_unit(course_key, unit_key)
    lesson = load_lesson(course_key, unit_key, lesson_key)
    grade_level = READING_LEVEL
    theme = course.theme
    unit_title = unit.title
    lesson_title = lesson.title
    topics = lesson.topics
    concepts = list_to_text(lesson.concepts)
    skills = list_to_text(lesson.skills)
    procedures = list_to_text(lesson.procedures)
    standards = unit_standards_to_text(lesson.standards)

    print("Generating Quiz: " + course_key + " " + unit_key + " " + lesson_key)
    quiz_prompt = prompt_lesson_quiz(
        grade_level=grade_level,
        theme=theme,
        unit_title=unit_title,
        lesson_title=lesson_title,
        topics=topics,
        concepts=concepts,
        skills=skills,
        procedures=procedures,
        standards=standards,
    )
    # print(quiz_prompt)

    lesson.prompt_quiz = quiz_prompt
    quiz_results = open_ai_submit_json(quiz_prompt, "Create Lesson Quiz", keys)
    save_lesson_quiz(
        course_key,
        unit_key,
        lesson_key,
        quiz_results["quiz_questions"],
    )
