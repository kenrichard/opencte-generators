# Split into Units & Lessons
#

from string import Template

LESSON_COUNT = 10


# Don't add a summary here or it starts truncating the outlines.
def get_prompt_unit_topics(unit_count, standards):
    t = Template(
        """
The following document contains a list of educational standards.

Organize the standards into a list of exactly $count1 topics.
There should be exactly $count1 topics, not more or fewer.
Give each topic a title that is similar but shorter than the original text.

Use titles that are similar to the standards, only shorter.

Standards:
$standards

Provide a  RFC8259 compliant JSON response following this format without deviation.
Any of your own explanations should be included in the JSON data.
{
  "topics": [{
    "topic": "The title of the topic",
  }],
  "explanations": "ChatGTP explanations about the prompt"
}
      """
    )
    return t.substitute(
        count1=unit_count,
        standards=standards,
    )


# Don't add a summary here or it starts truncating the outlines.
def get_prompt_unit_subtopics(topic, standards):
    t = Template(
        """
For the given topic, break it into $count2 subtopics. Use subtopics from the
list of provided standards when possible. Try to always create $count2 subtopics
by providing additional material related to the topic as needed.

The first topic should introduce the topic and help students understand
why the topic is important. The last topic should be a summary that reviews
the overall topic.

Use titles that are similar to the standards, only shorter.

Topic: $topic

Standards:
$standards

Provide a  RFC8259 compliant JSON response following this format without deviation.
Any of your own explanations should be included in the JSON data.
{
  "subtopics": {[
    "subtopic_title": "A list of subtopics for the topic",
  ]}
  "explanations": "ChatGTP explanations about the prompt"
}
      """
    )
    return t.substitute(
        count2=LESSON_COUNT,
        standards=standards,
        topic=topic,
    )


# Split into Units & Lessons
#
# Don't add a summary here or it starts truncating the outlines.
def get_prompt_course_summary():
    return """
The following document contains a list of educational standards.

Write a one or two sentence summary describing the main
themes of the course. Use a professional tone. The summary should
start with the words "Students will learn"

Provide a  RFC8259 compliant JSON response following this format without deviation.
Any of your own explanations should be included in the JSON data.
{
  "summary": "summary of the standards",
  "explanations": "ChatGTP explanations about the prompt"
}
        """
