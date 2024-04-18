"""Module providing Core ingest functions"""

from app.generators.course_ingest.prompts import ingest_prompt_csv
from app.models.course import save_new_course
from app.models.standards import save_course_standards
from app.utils.chatgpt import open_ai_submit_csv
from app.utils.resets import reset_course


def create_prompt(data):
    """Function to create prompt for ingest"""
    prompt = ingest_prompt_csv() + "\n\n" + data
    return prompt


def ingest(
    data, course_key, course_id, course_title, publisher, grade, theme, unit_count
):
    """Function to create prompt for ingest"""
    reset_course(course_key)

    prompt = create_prompt(data)

    print("== ingest PROMPT =====")
    print(prompt)
    standards = open_ai_submit_csv(prompt, "Ingest Standards")
    print("== STANDARDS =====")
    print(standards)
    print("== SAVING COURSE =====")
    save_new_course(
        course_key=course_key,
        course_id=course_id,
        course_title=course_title,
        publisher=publisher,
        grade=grade,
        theme=theme,
        unit_count=unit_count,
    )
    print("== SAVING STANDARDS =====")
    save_course_standards(course_key, standards)
