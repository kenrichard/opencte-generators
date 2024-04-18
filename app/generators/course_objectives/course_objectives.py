from prompts import prompt_course_objectives
from app.models.standards import load_standards
from app.utils.chatgpt import open_ai_submit_json


def course_objectives(course_key):
    keys = {"course_key": course_key}
    standards = load_standards(course_key)
    prompt = prompt_course_objectives(standards)
    # print(prompt)
    results = open_ai_submit_json(prompt, "Course Objectives", keys)
    for index, row in enumerate(results["objectives"]):
        print(str(index) + ". " + row)
