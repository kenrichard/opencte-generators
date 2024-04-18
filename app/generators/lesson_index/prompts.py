# Split into Units & Lessons
from string import Template


def prompt_summarize_lessons(lesson, content):
    t = Template(
        """
Write a short summary with about 200 words that provides an list of the main
topics covered in the course. Use paragraphs to make the summary easier to
read. Focus on including keywords that would
be relevant when searching for the lesson. Do not include the title of the lesson
or language saying this is a summary. Include a comma separated list of keywords
with the summary that will be used to index for search.

Lesson Title:
$title

Topic Covered:
$topics

Skills Covered:
$topics

Procedures Covered:
$procedures

Educational Standards:
$standards

Lesson Content:
$content

Provide a RFC8259 compliant JSON response following this format without deviation.
Any of your own explanations should be included in the JSON data.
{
  "summary": "Text summary of the lesson",
  "keywords": ["Keywords for indexing"]
  "explanations": "ChatGTP explanations about the prompt"
}
        """
    )

    return t.substitute(
        title=lesson.title,
        topics="\n".join(lesson.topics),
        procedures="\n".join(lesson.procedures),
        standards="\n".join(map(lambda x: x.standard, lesson.standards)),
        content="\n".join(content),
    )
