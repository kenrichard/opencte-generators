""" Data Model - Standard (Standards imported from text files) """

from app.utils.db_dynamo import (
    DynamoBase,
    dynamo_prefix_delete,
    dynamo_prefix_query,
    dynamo_save,
)


class Standard(DynamoBase):
    course_key: str
    standard_key: str
    standard: str
    seq: int


def standards_pk(course_key: str):
    return "COURSE~" + course_key


def standards_sk(standard_key: str):
    return "STANDARDS~" + standard_key


def save_course_standards(course_key, standards: list[Standard]):
    for index, standard in enumerate(standards):
        if len(standard) < 2:
            continue
        standard_key = standard[0]
        standard_text = ", ".join(standard[1:]).replace("  ", " ")
        print(standard_key + ". " + standard_text)
        new_standard = Standard(
            pk=standards_pk(course_key),
            sk=standards_sk(standard_key),
            course_key=course_key,
            standard_key=standard_key,
            standard=standard_text,
            seq=index,
        )
        dynamo_save(new_standard)


def load_standards(course_key):
    data = dynamo_prefix_query(standards_pk(course_key), standards_sk(""))
    return [Standard(**item) for item in data]


def delete_standards(course_key):
    dynamo_prefix_delete(standards_pk(course_key), standards_sk(""))
