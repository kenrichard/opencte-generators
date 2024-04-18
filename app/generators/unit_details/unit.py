import json
import logging
from app.utils.flatten import list_to_text
from app.utils.chatgpt import open_ai_submit_json
from app.models.standards import Standard, load_standards
from app.models.units import load_unit, update_unit
from .prompts import (
    prompt_units_standards,
    prompt_unit_skills,
    prompt_unit_summary,
)


def course_standard_mapper(standard: Standard):
    return ",".join(
        [
            standard.standard_key,
            '"' + standard.standard + '"',
        ]
    )


def course_standards_to_text(standards: list[Standard]):
    return "\n".join(map(lambda r: course_standard_mapper(r), standards))


def response_standard_mapper(standard):
    return ",".join(
        [
            standard["standard_key"],
            '"' + standard["standard"] + '"',
        ]
    )


def response_standards_to_text(standards):
    return "\n".join(map(response_standard_mapper, standards))


def expand_unit(course_key, unit_key):
    keys = {"course_key": course_key, "unit_key": unit_key}
    unit = load_unit(course_key, unit_key)
    unit_topics_text = "\n".join(unit.topics)
    course_standards = load_standards(course_key)
    course_standards_text = course_standards_to_text(course_standards)

    logging.debug("\n== UNIT TOPICS =====")
    logging.debug(unit_topics_text)

    ## GET STANDARDS
    standards_prompt = prompt_units_standards(
        unit_title=unit.title,
        unit_topics=unit_topics_text,
        course_standards=course_standards_text,
    )
    standards_results = open_ai_submit_json(
        standards_prompt, "Expand Unit 1/3 - Standards", keys
    )
    unit_standards = standards_results["standards"]
    unit_standards_text = response_standards_to_text(unit_standards)

    ## GET CONCEPTS/SKILLS
    skills_prompt = prompt_unit_skills(unit_standards_text)
    skills_results = open_ai_submit_json(
        skills_prompt, "Expand Unit 2/3 - Skills", keys
    )

    ## GET SUMMARY TEXT
    summary_prompt = prompt_unit_summary(
        unit_title=unit.title,
        unit_topics=unit_topics_text,
        unit_concepts=list_to_text(skills_results["concepts"]),
        unit_skills=list_to_text(skills_results["skills"]),
        unit_procedures=list_to_text(skills_results["procedures"]),
    )
    summary_results = open_ai_submit_json(
        summary_prompt, "Expand Unit 3/3 - Summary", keys
    )
    summary_text = summary_results["summary"]

    logging.debug("== RESULTS =====")
    logging.debug(json.dumps(standards_results, indent=4))
    logging.debug(json.dumps(skills_results, indent=4))
    logging.debug(json.dumps(summary_results))

    update_unit(
        course_key=course_key,
        unit_key=unit_key,
        standards=unit_standards,
        concepts=skills_results["concepts"],
        skills=skills_results["skills"],
        procedures=skills_results["procedures"],
        summary=summary_text,
    )

    logging.debug("== EXPLANATIONS =====")
    logging.debug(standards_results["explanations"])
    logging.debug(skills_results["explanations"])
    logging.debug(summary_results["explanations"])
