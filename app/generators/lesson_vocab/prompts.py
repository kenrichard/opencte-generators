from string import Template


def prompt_lesson_vocab(
    grade_level,
    theme,
    unit_title,
    lesson_title,
    topics,
    concepts,
    skills,
    procedures,
    standards,
    quiz,
):
    t = Template(
        """
You are a curriculum writer assigned to work on a lesson for $theme students.
You are creating a list of vocabulary words for a list of topics.
Choose the singular form for each word when possible.

Include vocabulary words and technical technical terms related to topics.
Include vocabulary words related to similar topics.
Include job roles and responsibilities related to the topics.
Include acronyms related to the topics
Include related and concepts student should understand.
Include words and acronyms that might not be known by a $grade_level grade student.

Include a brief definition of each vocabulary word.
Definitions should use vocabulary and phrases aligned a $grade_level grade reading level.
The words can be of any grade reading level.

For acronyms - The word should be the acronym without explanation and the meaning of the acronym should be in the definition.

Topics:
$unit_title
$lesson_title
$standards
$topics
$concepts
$skills
$procedures

Quiz Questions:
$quiz

Provide a  RFC8259 compliant JSON response following this format without deviation.
Any of your own explanations should be included in the JSON data.
{
  "vocabulary": [{"word","definition"}]
  "explanations": "Your explanations can go here"
}
        """
    )
    prompt = t.substitute(
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
    )
    return prompt
