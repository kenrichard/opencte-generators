# Split into Units & Lessons
from string import Template

COUNT = 6


def prompt_course_themes(standards):
    t = Template(
        """
Identify $count major topics from the following outline. For each theme
provide between 5 and 10 bullet points.

Standards
$standards

Provide a RFC8259 compliant JSON response following this format without deviation.
Any of your own explanations should be included in the JSON data.
{
  "themes": [{
    "theme": "the theme",
    "details: ["bullet points"]
  }]
  "explanations": "ChatGTP explanations about the prompt"
}
        """
    )

    return t.substitute(
        count=COUNT,
        standards=standards,
    )
