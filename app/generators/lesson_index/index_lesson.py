import json
from app.generators.lesson_index.prompts import prompt_summarize_lessons
from app.models.lessons import load_lesson, save_lesson, save_lesson_postgres
from app.utils.chatgpt import get_embedding, open_ai_submit_json


def index_lesson(course_key, unit_key, lesson_key):
    keys = {"course_key": course_key, "unit_key": unit_key, "lesson_key": lesson_key}
    lesson = load_lesson(course_key, unit_key, lesson_key)

    content = []
    for page in lesson.pages:
        for row in page.page_content:
            content.append(row)

    prompt = prompt_summarize_lessons(lesson, content)
    response = open_ai_submit_json(prompt, "Summarize Lesson", keys)

    lesson.summary = response["summary"]
    lesson.keywords = response["keywords"]
    lesson.embeddings_summary = json.dumps(
        get_embedding(lesson.summary, "Embedding: Lesson Summary", keys)
    )
    lesson.embeddings_keywords = json.dumps(
        get_embedding(",".join(lesson.keywords), "Embedding: Lesson Keywords", keys)
    )
    lesson.embeddings_text = json.dumps(
        get_embedding("\n".join(content), "Embedding: Lesson Text", keys)
    )

    save_lesson_postgres(lesson)

    # Don't save embeddings to dynamo
    lesson.embeddings_text = None
    lesson.embeddings_keywords = None
    lesson.embeddings_summary = None
    save_lesson(lesson)
