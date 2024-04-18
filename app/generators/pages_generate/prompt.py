from string import Template


def prompt_lesson_pages_v1(
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
You are a curriculum writer assigned to work on a lesson for $theme students.
The lesson should be written in a textbook style.
The course is divided into units and lessons.
The current unit is $unit_title.
The current lesson is $lesson_title.

Use vocabulary and phrases aligned a $grade_level grade reading level.

Create a set of pages for the lesson.
Cover all of the educational standards and topics.
Expand the standards and topics to provide a comprehensive introduction.
Include any vocabulary words or technical terms from the standards and topics.

The first page should introduce the lesson.
Each page should have a heading.
Each page should have 200 to 400 words, divided into paragraphs.
Each paragraph should have 50 to 100 words.
Add blank lines between paragraphs.

Standards:
$standards

Topics:
$topics


Include pages that cover each of the following concepts:
$concepts
$skills

Include a page for each of the following procedures. Procedure pages should include a bulleted list of steps required to complete the procedure.

Procedures:
$procedures

Provide a  RFC8259 compliant JSON response following this format without deviation.
Any of your own explanations should be included in the JSON data.
{
  "pages": [{
    "page_number": "the page number",
    "page_heading": "the main heading for the page",
    "page_content": ["list of paragraphs for the page"]
  }],
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


def prompt_lesson_pages_v2(
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
    vocab,
):
    t = Template(
        """
You are a curriculum writer assigned to work on a lesson for $theme students.
The lesson should be written in a textbook style.

The lesson is part of the topic: $unit_title
The title of the lesson is $lesson_title
Create a set of about $page_count pages for the lesson.

Use vocabulary and phrases aligned a $grade_level grade reading level.
Include vocabulary words and technical terms from the standards and topics.
Provide explanations of any job roles.

The first page should introduce the lesson with the phrases "Welcome to the exciting world" and "Let's Dive In"
Each page should have a heading.
Each page should have 200 to 400 words, divided into paragraphs.
Each paragraph should have 50 to 100 words.
Add blank lines between paragraphs.
Use double quotes instead of single quotes.
Try not to use too many exclamation points.

The following must be covered in the lesson:
$standards
$topics
$concepts
$skills
$procedures
$vocab
$quiz

Provide a  RFC8259 compliant JSON response following this format without deviation.
Any of your own explanations should be included in the JSON data.
{
  "pages": [{
    "page_number": "the page number",
    "page_heading": "the main heading for the page",
    "page_content": ["list of paragraphs for the page"]
  }],
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
        vocab=vocab,
        page_count=10,
    )
    return prompt
