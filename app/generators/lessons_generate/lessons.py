import logging
from app.models.course import load_course
from app.models.lessons import save_new_lessons
from app.utils.flatten import list_to_text, unit_standards_to_text
from app.utils.chatgpt import open_ai_submit_json
from app.models.units import load_unit, save_unit
from .prompts import prompt_define_lessons


def generate_lessons(course_key, unit_key):
    keys = {"course_key": course_key, "unit_key": unit_key}
    print(keys)
    course = load_course(course_key)
    unit = load_unit(course_key, unit_key)

    prompt = prompt_define_lessons(
        course_theme=course.theme,
        course_grade=course.grade,
        unit_title=unit.title,
        unit_summary=unit.summary,
        unit_standards=unit_standards_to_text(unit.standards),
        unit_topics=list_to_text(unit.topics),
        unit_concepts=list_to_text(unit.concepts),
        unit_skills=list_to_text(unit.skills),
        unit_procedures=list_to_text(unit.procedures),
    )
    # print(prompt)
    response = open_ai_submit_json(prompt, "Generate Lessons", keys)
    # print(response)

    save_new_lessons(course_key, unit_key, response)
    unit.lesson_count = len(response["lessons"])
    save_unit(unit)
