# Open CTE Generators

This code was prepared for a Tech Lancaster Meetup Talk. The code is incomplete
and designed to be used as an example.

## Workflows

### Step 1 - Ingest Standards

1. Creates Course
2. Saves Standards
3. Saves Course (ID & Title)

Once standards are ingested, you can use the --queue to automate the
rest of the processes.

### Step 3 - Course Themes

1. Create a list of high level topics for the course
2. Themes are the start of an assessment system - not used elsewhere

### Step 4 - Generate Outline

1. Identify Topics - Save as Units
2. For Each Unit - Identify SubTopics - Save with Unit in Database
3. Write a summary for the Unit

### Step 5 - Unit - Unit Details

1. Pull standards for this unit
2. Identify Skills/Concepts/Procedures
3. Write a Summary
4. Update Unit in Database

### Step 6 - Unit - Create Lessons

1. Define a set of lessons - What should be included in each
2. Save lesson stubs to the database

### Step 7 - Unit - Create Quiz

1. Create a set of quiz questions to assess the lesson

### Step 8 - Unit - Create Vocab

1. Create a list of vocabulary words for the lesson

### Step 9 - Unit - Create Vocab

1. Create page content for the lesson

### Step 10 - Unit - Translate Lessons

1. Create spanish versions of the lessons

### Step 11 - Write a summary

1. Write a summary
2. Get embeddings
3. Save in PostGres for vector search

