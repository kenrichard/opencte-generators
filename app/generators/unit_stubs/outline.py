import json
import logging
from app.models.course import load_course, update_course_summary
from app.utils.chatgpt import open_ai_submit_json
from app.utils.flatten import course_standards_to_text_no_numbers
from app.utils.resets import reset_outline
from app.models.standards import load_standards
from app.models.units import save_new_unit
from .prompts import (
    get_prompt_course_summary,
    get_prompt_unit_topics,
    get_prompt_unit_subtopics,
)


def generate_outline(course_key):
    keys = {"course_key": course_key}

    # Clear Old Data
    reset_outline(course_key)

    course = load_course(course_key)
    standards = load_standards(course_key)
    standards_string = course_standards_to_text_no_numbers(standards)
    topics_prompt = get_prompt_unit_topics(course.unit_count, standards_string)

    print("== TOPICS PROMPT ==")
    print(topics_prompt)

    topics = open_ai_submit_json(
        topics_prompt, "Create Course Outline - Get Topics", keys
    )

    print("== EXPLANATIONS =====")
    print(topics["explanations"])

    print("== TOPICS ==")
    print(json.dumps(topics, indent=2))

    for index, row in enumerate(topics["topics"]):
        subtopics_prompt = get_prompt_unit_subtopics(row["topic"], standards_string)

        print("== SUBTOPICS PROMPT " + str(index + 1) + " ==")
        print(subtopics_prompt)

        subtopics = open_ai_submit_json(
            subtopics_prompt, "Create Course Outline - Unit " + str(index + 1), keys
        )

        print("== SUBTOPICS " + str(index + 1) + " RESULTS ==")
        print(json.dumps(subtopics, indent=2))

        subtopic_list = map(lambda x: x["subtopic_title"], subtopics["subtopics"])
        save_new_unit(course_key, index, row["topic"], subtopic_list)

    summary_prompt = get_prompt_course_summary() + "\n\n" + json.dumps(topics["topics"])
    summary = open_ai_submit_json(summary_prompt, "Create Course Outline 2/2", keys)

    update_course_summary(course_key, summary["summary"])
