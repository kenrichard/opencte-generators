from app.models.lessons import LessonQuestion, LessonVocab
from app.models.standards import Standard
from app.models.units import UnitStandard


def list_to_text(list):
    return ",".join(list)


def unit_standard_mapper(standard: UnitStandard):
    return ",".join(
        [
            standard.standard_key,
            '"' + standard.standard + '"',
        ]
    )


def unit_standards_to_text(standards: list[UnitStandard]):
    return "\n".join(map(lambda r: unit_standard_mapper(r), standards))


def course_standard_mapper(standard: Standard):
    return ",".join(
        [
            standard.standard_key,
            '"' + standard.standard + '"',
        ]
    )


def course_standards_to_text(standards: list[Standard]):
    return "\n".join(map(course_standard_mapper, standards))


def course_standards_to_text_no_numbers(standards: list[Standard]):
    return "\n".join(map(lambda x: x.standard, standards))


def quiz_question_mapper(question: LessonQuestion):
    return question.question_text


def quiz_questions_to_text(questions: list[LessonQuestion]):
    return "\n".join(map(quiz_question_mapper, questions))


def vocab_mapper(v: LessonVocab):
    return v.word


def vocab_to_text(questions: list[LessonVocab]):
    return "\n".join(map(vocab_mapper, questions))
