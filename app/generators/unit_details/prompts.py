from string import Template


#
# Match Standards for the Unit
#
def prompt_units_standards(unit_title, unit_topics, course_standards):
    t = Template(
        """
The following topics and subtopics are for a chapter
in an educational textbook.

Scan the list of educational standards at the bottom of the
document and provide a list of standards that could be covered
by the topic.

Topic: $unit_title

Subtopics:
$unit_topics

Standards:
$course_standards

Provide a  RFC8259 compliant JSON response following this format without deviation.
Any of your own explanations should be included in the JSON data.
{
  standards: [{
    "standard_key": "The unique identifier for the standards",
    "standard": "The text for the standard".
  }]
  "explanations": "ChatGTP explanations about the prompt"
}
        """
    )
    return t.substitute(
        unit_title=unit_title,
        unit_topics=unit_topics,
        course_standards=course_standards,
    )


#
# Identify Concepts, Skills & Procedures for Unit
#
def prompt_unit_skills(unit_standards):
    t = Template(
        """
Review the educational standards below.

Evaluate the content and determine if there are any
concepts or skills, skills, or procedures.

Create a list of concepts the student should understand.
Create a list of skills the student should acquire.
Create a list of hands-on procedures the student should be able to perform.

Standards:
$unit_standards

Provide a  RFC8259 compliant JSON response following this format without deviation.
Any of your own explanations should be included in the JSON data.
{
  "concepts": ["a list of concepts"],
  "skills": ["a list of skills"],
  "procedures": ["a list of procedures"],
  "explanations": "Your explanations can go here"
}
        """
    )
    prompt = t.substitute(unit_standards=unit_standards)

    return prompt


# Generate summary
def prompt_unit_summary(
    unit_title, unit_topics, unit_concepts, unit_skills, unit_procedures
):
    t = Template(
        """
You are working on a unit of digital curriculum.
Process the following and write a two sentence summary of what the student will learn.
Use a professional tone. The summary should start with the words "Students will learn"

Topics the content will cover
$unit_topics

Concepts the student should understand:
$unit_concepts

Skills the student should acquire:
$unit_skills

Procedures the student should be able to perform:
$unit_procedures

Provide a  RFC8259 compliant JSON response following this format without deviation.
Any of your own explanations should be included in the JSON data.
{
  "summary": "the summary text",
  "explanations": "ChatGTP explanations about the prompt"
}
        """
    )
    return t.substitute(
        unit_title=unit_title,
        unit_topics=unit_topics,
        unit_concepts=unit_concepts,
        unit_skills=unit_skills,
        unit_procedures=unit_procedures,
    )
