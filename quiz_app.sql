CREATE DATABASE quiz_app;

USE quiz_app;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    username VARCHAR(255) UNIQUE,
    phone_no VARCHAR(10),
    password VARCHAR(255),
    enrollment_no VARCHAR(255)
);

CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    section VARCHAR(255),
    question TEXT,
    option1 TEXT,
    option2 TEXT,
    option3 TEXT,
    answer INT
);

CREATE TABLE scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255),
    section VARCHAR(255),
    score INT
);

INSERT INTO questions (section, question, option1, option2, option3, answer) 
VALUES 
('DSA', 'What does LIFO stand for?', 'Last In First Out', 'First In Last Out', 'Last In First Only', 1),
('DSA', 'Which data structure is used in recursion?', 'Queue', 'Stack', 'Heap', 2),
('DSA', 'What is the time complexity of binary search?', 'O(n)', 'O(n^2)', 'O(log n)', 3);

INSERT INTO questions (section, question, option1, option2, option3, answer) 
VALUES 
('DBMS', 'What does SQL stand for?', 'Structured Query Language', 'Sequential Query Language', 'Structured Quick Language', 1),
('DBMS', 'Which key uniquely identifies a row in a table?', 'Primary Key', 'Foreign Key', 'Candidate Key', 1),
('DBMS', 'What is a foreign key?', 'Key that links two tables', 'Key that uniquely identifies a row', 'Key used for indexing', 1);

INSERT INTO questions (section, question, option1, option2, option3, answer) 
VALUES 
('Python', 'Which keyword is used to define a function in Python?', 'def', 'function', 'lambda', 1),
('Python', 'What is the output of print(2 ** 3)?', '6', '8', '9', 2),
('Python', 'Which of the following is not a data type in Python?', 'List', 'Tuple', 'ArrayList', 3);
