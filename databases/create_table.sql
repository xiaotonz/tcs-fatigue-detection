CREATE DATABASE [IF NOT EXISTS] employee_db

CREATE TABLE EMPLOYEE(
    emp_id varchar(255) PRIMARY KEY,
    emp_name varchar(255),
    emp_position varchar(255),
    emp_shift int
);


CREATE TABLE EMPLOYEE(
    emp_id varchar(255) PRIMARY KEY,
    emp_name varchar(255),
    emp_position varchar(255),
    emp_shift int
);

CREATE TABLE FATIGUE_HISTORY (
    IDColumn INT AUTO_INCREMENT PRIMARY KEY,
    created_at VARCHAR(255),
    emp_id VARCHAR(255),
    FOREIGN KEY (emp_id) REFERENCES EMPLOYEE(emp_id)
);


CREATE TABLE FATIGUE_HISTORY_INDEX (
    IDColumn INT AUTO_INCREMENT PRIMARY KEY,
    created_at VARCHAR(255),
    emp_id VARCHAR(255),
    fatigue_index FLOAT,
    FOREIGN KEY (emp_id) REFERENCES EMPLOYEE(emp_id)
);
