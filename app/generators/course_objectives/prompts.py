# Split into Units & Lessons
from string import Template


def prompt_course_objectives(standards):
    t = Template(
        """
Review the following educational standards document and break things down into
a detailed list specific things students need to learn. From that list,
defined learning objectives using Bloom's Taxonomy.

Standards
$standards

Provide a RFC8259 compliant JSON response following this format without deviation.
Any of your own explanations should be included in the JSON data.
{
  "objectives": ["list of learning objectives"]
  "explanations": "ChatGTP explanations about the prompt"
}
        """
    )

    return t.substitute(
        standards="\n".join(map(lambda x: x.standard, standards)),
    )
