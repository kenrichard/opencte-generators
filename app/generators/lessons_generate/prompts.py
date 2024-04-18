# Split into Units & Lessons
from string import Template


def prompt_define_lessons(
    course_theme,
    course_grade,
    unit_title,
    unit_summary,
    unit_standards,
    unit_topics,
    unit_concepts,
    unit_skills,
    unit_procedures,
):
    t = Template(
        """
You are working on an $course_theme educational course for $course_grade students.
The course is divided into units and lessons.
The information below is the requirements for the unit.

Review the title, summary, standards and topics for the unit.
Organize the topics into a set of lessons for the unit.
The first lesson should be an introductory lesson.

For each lesson, create a list of topics that are related to the standards.
For each lesson, create a list of concepts that are related to the standards.
For each lesson, create a list of skills that are related.
For each lesson, create a list of procedures that are related.

Expand the topics, concepts, skills and procedures to provide a comprehensive introduction.

Unit Title:
$unit_title

Unit Summary:
$unit_summary

Unit Standards:
$unit_standards

Unit Topics:
$unit_topics

Unit Concepts:
$unit_concepts

Unit Skills:
$unit_skills

Unit Procedures:
$unit_procedures

Provide a RFC8259 compliant JSON response following this format without deviation.
Any of your own explanations should be included in the JSON data.
{
  "lessons": [{
    "title": "the title of the lesson",
    "topics": ["a list of topics for the lesson"],
    "concepts": ["a list of concepts for the lesson"],
    "skills": ["a list of skills for the lesson"],
    "procedures": ["a list of procedures for the lesson"],
    "standards": [{
      "standard_key": "the unique identifier of the standard",
      "standard": "the text for the standard",
    }]
  }]
  "explanations": "ChatGTP explanations about the prompt"
}
        """
    )
    return t.substitute(
        course_theme=course_theme,
        course_grade=course_grade,
        unit_title=unit_title,
        unit_summary=unit_summary,
        unit_standards=unit_standards,
        unit_topics=unit_topics,
        unit_concepts=unit_concepts,
        unit_skills=unit_skills,
        unit_procedures=unit_procedures,
    )
