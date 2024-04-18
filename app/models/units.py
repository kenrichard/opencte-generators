""" Data Model - Unit (Course has set of Units; Unit has set of lessons) """

import logging
import datetime
from typing import Optional
from app.utils.db_dynamo import (
    DynamoBase,
    dynamo_load,
    dynamo_prefix_delete,
    dynamo_prefix_query,
    dynamo_save,
)

##
## UNITS
##


class UnitStandard(DynamoBase):
    standard_key: str
    standard: str


class Unit(DynamoBase):
    course_key: str
    unit_key: str
    title: str
    summary: Optional[str] = None
    standards: Optional[list[UnitStandard]] = None
    topics: Optional[list[str]] = None
    concepts: Optional[list[str]] = None
    skills: Optional[list[str]] = None
    procedures: Optional[list[str]] = None
    lesson_count: Optional[int] = 0
    ts: Optional[str] = None
    seq: int


def unit_pk(course_key: str):
    return "COURSE~" + course_key


def unit_sk(unit_key: str):
    return "UNIT~" + unit_key


def save_unit(unit: Unit):
    unit.pk = unit_pk(unit.course_key)
    unit.sk = unit_sk(unit.unit_key)
    dynamo_save(unit)


def load_unit(course_key: str, unit_key: str):
    data = dynamo_load(unit_pk(course_key), unit_sk(unit_key))
    logging.debug("Loading Unit")
    logging.debug(data)
    return Unit(**data)


def load_units(course_key: str):
    data = dynamo_prefix_query(unit_pk(course_key), unit_sk(""))
    units = [Unit(**row) for row in data]
    return units


def delete_units(course_key):
    dynamo_prefix_delete(unit_pk(course_key), unit_sk(""))


def save_new_unit(course_key, index, topic, subtopics):
    logging.debug("\nSAVING UNIT")
    unit_key = "U%03d" % (index + 1,)
    unit_title = topic
    unit_topics = subtopics

    unit = Unit(
        pk=unit_pk(course_key),
        sk=unit_sk(unit_key),
        course_key=course_key,
        unit_key=unit_key,
        title=unit_title,
        topics=unit_topics,
        seq=index,
        ts=datetime.datetime.now().astimezone().isoformat(),
    )

    logging.debug(unit)
    dynamo_save(unit)


def update_unit(
    course_key,
    unit_key,
    standards,
    concepts,
    skills,
    procedures,
    summary,
):
    unit = load_unit(course_key, unit_key)
    unit.standards = [UnitStandard(**s) for s in standards]
    unit.concepts = concepts
    unit.skills = skills
    unit.procedures = procedures
    unit.summary = summary
    unit.ts = datetime.datetime.now().astimezone().isoformat()
    save_unit(unit)
