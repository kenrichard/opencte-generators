import boto3
from app.models.lessons import load_lesson, save_lesson


def translate_text(text, target_language):
    # Initialize the AWS Translate client
    translate = boto3.client("translate")

    # Call AWS Translate to translate the text
    try:
        response = translate.translate_text(
            Text=text, SourceLanguageCode="en", TargetLanguageCode=target_language
        )
        return response.get("TranslatedText")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def translate_lesson(lesson):
    for page in lesson.pages:
        page.page_content_es = []
        page.page_heading_es = translate_text(page.page_heading, "es-MX")
        for content in page.page_content:
            output = translate_text(content, "es-MX")
            page.page_content_es.append(output)
    lesson.retranslate_lesson = False
    save_lesson(lesson)
