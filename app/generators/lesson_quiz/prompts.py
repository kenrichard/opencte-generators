from string import Template


def prompt_lesson_quiz(
    grade_level,
    theme,
    unit_title,
    lesson_title,
    topics,
    concepts,
    skills,
    procedures,
    standards,
):
    t = Template(
        """
You are working on text for a $grade_level educational course for $theme.
The course is divided into units and lessons.
The current unit is $unit_title.
The current lesson is $lesson_title.
Use vocabulary and phrases aligned a $grade_level grade reading level.

Write 10 quiz questions to evaluate student's understanding of the standards, topics and concepts.
Include questions about vocabulary words or technical terms from the standards and topics.
Each question should have 4 multiple choice options.

Use terms without quotes when possible. If quotes are needed use double quotes instead of single quotes.

Standards:
$standards

Topics:
$topics

Concepts:
$concepts

Provide a  RFC8259 compliant JSON response following this format without deviation.
Any of your own explanations should be included in the JSON data.
{
"quiz_questions": [{
  "question_number": "the number of the quiz question",
  "question_text": "the text of the quiz question",
  "quiz_choices": [{
      "choice": "The text for a quiz choice",
      "correct": "Indicates yes or no if the question is the correct choice"
  }]
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
    )
    return prompt
