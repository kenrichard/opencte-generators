from app.generators.lesson_vocab.prompts import prompt_lesson_vocab
from app.generators.pages_generate.pages import READING_LEVEL
from app.generators.pages_translate.translate import translate_text
from app.models.course import load_course
from app.models.lessons import LessonVocab, load_lesson, save_lesson
from app.models.units import load_unit
from app.utils.chatgpt import open_ai_submit_json
from app.utils.flatten import (
    list_to_text,
    quiz_questions_to_text,
    unit_standards_to_text,
)


def generate_vocab(course_key, unit_key, lesson_key):
    print("generate_vocab", course_key, unit_key, lesson_key)

    keys = {
        "course_key": course_key,
        "unit_key": unit_key,
        "lesson_key": lesson_key,
    }

    course = load_course(course_key)
    unit = load_unit(course_key, unit_key)
    lesson = load_lesson(course_key, unit_key, lesson_key)
    grade_level = READING_LEVEL  # course.grade
    theme = course.theme
    unit_title = unit.title
    lesson_title = lesson.title
    topics = lesson.topics
    concepts = list_to_text(lesson.concepts)
    skills = list_to_text(lesson.skills)
    procedures = list_to_text(lesson.procedures)
    standards = unit_standards_to_text(lesson.standards)
    quiz = quiz_questions_to_text(lesson.quiz_questions)

    prompt = prompt_lesson_vocab(
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
    # print(prompt)

    results = open_ai_submit_json(prompt, "Lesson Vocab", keys)
    lesson.vocab = []
    for row in results["vocabulary"]:
        print(row)

        word = row["word"]
        definition = row["definition"]

        word_es = translate_text(word, "es-MX")
        definition_es = translate_text(definition, "es-MX")

        lesson.vocab.append(
            LessonVocab(
                word=word,
                definition=definition,
                word_es=word_es,
                definition_es=definition_es,
            )
        )
    save_lesson(lesson)
