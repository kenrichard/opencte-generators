## CSV works better than JSON for this example.
## The JSON version says it's out of tokens and returns
## a partial result.


def ingest_prompt_csv():
    return """
The following contains an outline for standards for an educational course.
Organize into a two level numbered outline of topics and subtopics.
Smaller topics can be combined to enforce two levels.
Do not summarize. Include the original text whenever possible.

Format the dataset as a csv with the first column as the unique identifier and the second column as the text.
Do not include any explanations. The output should only be the CSV data.
Do not include column headers for the CSV.
    """
