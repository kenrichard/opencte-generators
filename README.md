# EZAuthors - API

## Workflows

### OVERVIEW

1. Ingest - Parse Standards
  a. Creates Course
  b. Saves Standards
  c. Saves Course (ID & Title)
2. Outline - Create Unit Stubs
  a. Takes Course Standards
  b. Creates Topics/Subtopics
  c. Topics become Units
  d. Generates Summary
  e. Subtopics saved as "topics" for the unit
  f. Saves Units (Title, Topics)
  g. Saves Course (Update Summary)
3. Unit - Details for one unit
  a. Gets Standards for the Topics
  b. Identifies Concepts, Skills, Procedures
  c. Writes a summary for the unit
  d. Saves Unit (updates data)
4. Lessons - Creates Lesson Stubs
  a. Creates New Lessons (no pages)
  b. Finds standards, topics, concepts, skills, and procedures for each lesson
4. Pages - Create Page Content for Lessons
  a. Updates Lessons


## ingest

```
python main.py ingest \
--input data/standards/fl-dit-8207310.txt \
--course_key=FL-BIT-DIT-8207310 \
--course_id=8207310 \
--course_title="Digital Information Technology" \
--publisher="Florida"
```

```
python main.py ingest \
--input data/standards/fl-ma-01-basic-health-care-worker.txt  \
--course_key="FL-MA-01" \
--course_id="31-9099" \
--course_title="Basic Healthcare Worker" \
--publisher="Florida"
```

```
python main.py ingest \
--input data/standards/fl-health-ms-8400310.txt  \
--course_key="FL-HS-8400310" \
--course_id="8400310" \
--course_title="Exploration of Health Science Professions" \
--publisher="Florida" \
--grade="7th" \
--theme="Health Science Introduction"
```

```
python main.py ingest \
--input data/standards/TX-130.222_Principles.txt  \
--course_key="TX-HS-130.222" \
--course_id="130.222" \
--course_title="Principles of Health Science" \
--publisher="Texas" \
--grade="9th" \
--theme="Health Science Foundation"
```

```
python main.py ingest \
--input data/standards/fl-8500120-personal-finance.txt  \
--course_key="FL-PF-8500120" \
--course_id="8500120" \
--course_title="Personal Financial Literacy" \
--publisher="Florida" \
--grade="6th" \
--theme="Career Readiness"
```

```
python main.py ingest \
--input data/standards/nchse-framework.txt  \
--course_key="NCHSE-Framework" \
--course_id="NCHSE" \
--course_title="National Health Science Curriculum" \
--publisher="NCHSE" \
--grade="9th" \
--theme="Health Science Foundations"
```

```
python main.py ingest \
--input "data/standards/Certiport - Entrepreneurial and Small Business.txt"  \
--course_key="NCHSE-ESB-V.2" \
--course_id="ESB-V.2" \
--course_title="Entrepreneurial and Small Business" \
--publisher="Certiport" \
--grade="9th" \
--theme="Business Fundamentals"
```

## Outline

python main.py outline --course_key="FL-BIT-DIT-8207310"
python main.py outline --course_key="FL-MA-01"
python main.py outline --course_key="FL-HS-8400310"

 ## Units

python main.py unit --course_key="FL-BIT-DIT-8207310" --unit_key="U001"
python main.py unit --course_key="FL-MA-01" --unit_key="U001"
python main.py unit --course_key="FL-HS-8400310" --unit_key="U001"

## Lessons

python main.py lessons --course_key="FL-BIT-DIT-8207310" --unit_key="U001"
python main.py lessons --course_key="FL-MA-01" --unit_key="U001"
python main.py lessons --course_key="FL-HS-8400310" --unit_key="U001"

## Pages

python main.py pages --course_key="FL-BIT-DIT-8207310" --unit_key="U001" --lesson_key="L001"
python main.py pages --course_key="FL-MA-01" --unit_key="U001" --lesson_key="L001"
python main.py pages --course_key="FL-HS-8400310" --unit_key="U001" --lesson_key="L001"








 python main.py lessons --course_key=ESBV2 --unit_key=U003
 python main.py lessons --TX-HS-130.222 --unit_key=U002
 python main.py lessons --NCHSE-Framework --unit_key=U002
 python main.py lessons --FL-PF-8500120 --unit_key=U002
 python main.py lessons --FL-MA-01 --unit_key=U002
 python main.py lessons --FL-HS-8400310 --unit_key=U002
 python main.py lessons --FL-BIT-DIT-8207310 --unit_key=U002
