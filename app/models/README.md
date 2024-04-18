# Database Schema

Data is stored in Dynamo and Postgresql. Dynamo is the main
data store for all data. Postgresql is used to index content
for vector search.

## Dynamo

We use a simple system where "pk" is the partition key,
"sk" is the sort key, and "lk" (lookup key) is an optional
global secondary index.

## Model Objects

Each model object has a set of utility functions to help with
the keys.

For example:

```
def lesson_pk(course_key: str):
    return "COURSE~" + course_key

def lesson_sk(unit_key: str, lesson_key: str):
    return LESSON_SK_PREFIX + unit_key + "~" + lesson_key
```

These helpers are used within the load and save functions for
that data object.

```
def load_course(course_key) -> Course:
    data = dynamo_load(course_pk(), course_sk(course_key))
    return Course(**data)

def save_course(course: Course):
    course.pk = course_pk()
    course.sk = course_sk(course.course_key)
    dynamo_save(course)
```

## Postgresql

We also save a copy of some objects to Postgresql for vector search.
Embeddings are generated with openai and saved with pgvector.


