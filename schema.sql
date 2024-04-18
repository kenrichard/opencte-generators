/*
 * Postgresql Schema for vector search
 */

CREATE EXTENSION vector;


/* RESET */
createdb ezauthors;
DROP TABLE courses;
DROP TABLE standards;
DROP table topics;
DROP table lessons;
DROP table page_feedback;

/* STANDARDS */
CREATE TABLE standards (
  id bigserial PRIMARY KEY,
  course_key varchar(255),
  standard_key varchar(255),
  content text,
  seq numeric,
  embedding vector(1536)
);

/* COURSES */
CREATE TABLE courses (
  id bigserial PRIMARY KEY,
  course_key varchar(255),
  course_id varchar(255),
  title varchar(255),
  summary text,
  theme varchar(255),
  grade varchar(255),
  lesson_minutes varchar(255),
  publisher varchar(255)
);

/* UNITS */
CREATE TABLE units (
  id bigserial PRIMARY KEY,
  course_key varchar(255),
  unit_key varchar(255),
  title varchar(255),
  summary text,
  standards json,
  topics json,
  concepts json,
  skills json,
  procedures json,
  seq numeric,
  embedding vector(1536)
);

/* LESSONS */
CREATE TABLE lessons (
  id bigserial PRIMARY KEY,
  course_key varchar(255),
  unit_key varchar(255),
  lesson_key varchar(255),
  title varchar(255),
  summary text,
  topics json,
  concepts json,
  skills json,
  procedures json,
  unit_title varchar(255),
  course_title varchar(255),
  course_theme varchar(255),
  course_grade varchar(255),
  course_publisher varchar(255),
  embeddings_summary vector(1536),
  embeddings_keywords vector(1536),
  embeddings_text vector(1536)
);

