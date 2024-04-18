from app.generators.course_themes.course_themes import course_themes
from app.generators.lesson_quiz.quiz import generate_quiz
from app.generators.lesson_vocab.vocab import generate_vocab
from app.models.course import load_all_courses
from app.models.lessons import load_lessons
from app.models.units import load_units

from app.generators.unit_stubs.outline import generate_outline
from app.generators.lesson_index.index_lesson import index_lesson
from app.generators.lessons_generate.lessons import generate_lessons
from app.generators.pages_generate.pages import generate_pages
from app.generators.pages_translate.translate import translate_lesson
from app.generators.unit_details.unit import expand_unit

#
# Load All Courses - For Each:
#
# 1 Course Theme (For Self Assessments)
# 2 Course Outline / Unit Stubs

DEFAULT_LOOPS = 1
COURSE_FILTER = ["FL-PF-8500120", "FL-BIT-DIT-8207310", "FL-MA-01"]
UNIT_FILTER = []
LESSON_FILTER = []

TRANSLATE_LESSONS = False


def create_queue_subparser(subparsers):
    parser = subparsers.add_parser("queue")
    parser.add_argument("--debug")
    parser.add_argument("--loops", type=int)


# Returns TRUE if there is not a filter
# Returns TRUE if the item doesn't have filtered attribute
# Returns FALSE if the item doesn't match the filter
def check_course_filter(object):
    # Is there a filter?
    if len(COURSE_FILTER) == 0:
        return True
    # Does the object have the filtered attribute?
    if not hasattr(object, "course_key"):
        return True
    # Check the filter - Return FALSE it no hit
    if object.course_key not in COURSE_FILTER:
        return False
    return True


def check_course_themes(object):
    if object.themes is not None:
        return False
    if check_course_filter(object) is False:
        return False
    return True


# Returns TRUE if there is not a filter
# Returns TRUE if the item doesn't have filtered attribute
# Returns FALSE if the item doesn't match the filter
def check_unit_filter(object):
    # Is there a filter?
    if len(UNIT_FILTER) == 0:
        return True
    # Does the object have the filtered attribute?
    if not hasattr(object, "unit_key"):
        return True

    # Check the filter - Return FALSE it no hit
    if object.unit_key not in UNIT_FILTER:
        return False
    return True


# Returns TRUE if there is not a filter
# Returns TRUE if the item doesn't have filtered attribute
# Returns FALSE if the item doesn't match the filter
def check_lesson_filter(object):
    # Is there a filter?
    if len(LESSON_FILTER) == 0:
        return True
    # Does the object have the filtered attribute?
    if not hasattr(object, "lesson_key"):
        return True
    # Check the filter - Return FALSE it no hit
    if object.lesson_key not in LESSON_FILTER:
        return False
    return True


def check_should_quiz(lesson):
    if check_course_filter(lesson) is False:
        return False
    if check_unit_filter(lesson) is False:
        return False
    if lesson.quiz_questions is None:
        return True
    return False


def check_should_generate(lesson):
    if check_course_filter(lesson) is False:
        return False
    if check_unit_filter(lesson) is False:
        return False
    if lesson.rebuild_lesson:
        return True
    if lesson.pages is None:
        return True
    return False


def check_should_translate(lesson):
    if TRANSLATE_LESSONS is False:
        return False
    if lesson.pages is None or len(lesson.pages) == 0:
        return False
    if check_course_filter(lesson) is False:
        return False
    if "retranslate_lesson" in lesson and lesson.retranslate_lesson:
        return True
    if lesson.pages[0].page_content_es is None:
        return True
    return False


def check_should_summarize(lesson):
    # Make sure we have content first
    if lesson.pages is None or len(lesson.pages) == 0:
        return False
    # Already summarized?
    if lesson.summary:
        return False
    if check_course_filter(lesson) is False:
        return False
    if check_unit_filter(lesson) is False:
        return False
    return True


def check_should_create_vocab(lesson):
    # Already has vocab?
    if lesson.vocab:
        return False
    if check_course_filter(lesson) is False:
        return False
    if check_unit_filter(lesson) is False:
        return False
    return True


def process_queue(args):
    # units = load_units("FL-PF-8500120")
    # for unit in units:
    #     lessons = load_lessons(unit.course_key, unit.unit_key)
    #     for lesson in lessons:
    #         print(lesson.unit_key + " " + lesson.lesson_key)
    #         lesson.rebuild_lesson = True
    #         save_lesson(lesson)
    if args.loops:
        loops = args.loops
    else:
        loops = DEFAULT_LOOPS
    for i in range(loops):
        print("LOOP " + str(i + 1) + "/" + str(loops))
        if check_courses() == False:
            return


# Return True when something is processed
def check_courses():
    courses = load_all_courses()
    for course in courses:
        if check_course_filter(course) is False:
            print("Skipping Course " + course.course_key)
            continue
        if check_course_themes(course) is True:
            print("QUEUE - Course Themes - " + course.course_key)
            course_themes(course.course_key)
            return True
        units = load_units(course.course_key)
        if len(units) == 0:
            print("QUEUE - Course Outline - " + course.course_key)
            generate_outline(course.course_key)
            return True
        for unit in units:
            if check_unit(unit):
                return True
    return False


# Return True when something is processed
def check_unit(unit):
    if check_unit_filter(unit) is False:
        print("QUEUE - Skip Unit " + unit.course_key + " " + unit.unit_key)
        return False

    if unit.summary is None:
        print("QUEUE - Expand Unit " + unit.course_key + " " + unit.unit_key)
        expand_unit(unit.course_key, unit.unit_key)
        return True

    lessons = load_lessons(unit.course_key, unit.unit_key)
    if len(lessons) == 0:
        print("QUEUE - Create Lessons " + unit.course_key + " " + unit.unit_key)
        generate_lessons(unit.course_key, unit.unit_key)
        return True

    for lesson in lessons:
        if check_lesson(lesson):
            return True


def check_lesson(lesson):
    if check_lesson_filter(lesson) is False:
        return False
    if check_should_quiz(lesson):
        generate_quiz(lesson.course_key, lesson.unit_key, lesson.lesson_key)
        return True
    if check_should_create_vocab(lesson):
        print(
            f"QUEUE - Create Lesson Vocab {lesson.course_key} {lesson.unit_key} {lesson.lesson_key}"
        )
        generate_vocab(lesson.course_key, lesson.unit_key, lesson.lesson_key)
        return True
    if check_should_generate(lesson):
        print(
            f"QUEUE - Create Pages {lesson.course_key} {lesson.unit_key} {lesson.lesson_key}"
        )
        generate_pages(lesson.course_key, lesson.unit_key, lesson.lesson_key)
        return True
    if check_should_translate(lesson):
        print(
            f"QUEUE - Translate Pages {lesson.course_key} {lesson.unit_key} {lesson.lesson_key}"
        )
        translate_lesson(lesson)
        return True
    if check_should_summarize(lesson):
        print(
            f"QUEUE - Summarize Lesson {lesson.course_key} {lesson.unit_key} {lesson.lesson_key}"
        )
        index_lesson(lesson.course_key, lesson.unit_key, lesson.lesson_key)
        return True

    return False


# FL-MA-01
# FL-PF-8500120
# FL-BIT-DIT-8207310
