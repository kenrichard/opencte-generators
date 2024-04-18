from app.generators.course_themes.prompts import prompt_course_themes
from app.models.course import CourseThemes, load_course, save_course
from app.models.standards import load_standards
from app.utils.chatgpt import open_ai_submit_json
from app.utils.flatten import course_standards_to_text


def course_themes(course_key):
    keys = {"course_key": course_key}
    standards = load_standards(course_key)
    course_standards_text = course_standards_to_text(standards)

    prompt = prompt_course_themes(course_standards_text)
    # print(prompt)
    results = open_ai_submit_json(prompt, "Course Themes", keys)
    # print(results)

    course = load_course(course_key)
    course.themes = []
    for row in results["themes"]:
        # print("==============================")
        # print(row)
        course.themes.append(CourseThemes(theme=row["theme"], details=row["details"]))

    # print("==== THEMES ==========================")
    # print(course.themes)
    save_course(course)
