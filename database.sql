CREATE DATABASE ces_db;

USE ces_db;

CREATE TABLE students(
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100),
    email VARCHAR(100),
    department VARCHAR(50)
);

CREATE TABLE courses(
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100),
    instructor VARCHAR(100),
    duration VARCHAR(50)
);

CREATE TABLE enrollments(
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    course_id INT,
    enrollment_date DATE,
    FOREIGN KEY(student_id) REFERENCES students(student_id),
    FOREIGN KEY(course_id) REFERENCES courses(course_id)
);
select * from students;

ALTER TABLE enrollments
ADD CONSTRAINT unique_student_course
UNIQUE (student_id, course_id);

SELECT
    student_id,
    course_id,
    COUNT(*) AS total
FROM enrollments
GROUP BY student_id, course_id
HAVING COUNT(*) > 1;

ALTER TABLE courses
ADD COLUMN capacity INT NOT NULL DEFAULT 30;

UPDATE courses
SET capacity = 50
WHERE course_name = 'Python';

UPDATE courses
SET capacity = 40
WHERE course_name = 'SQL';
