CREATE TABLE contacts (
	id SERIAL PRIMARY KEY,
	last_name VARCHAR(100),
	first_name VARCHAR(100) NOT NULL,
	middle_name VARCHAR(100),
	phone_number VARCHAR(20) NOT NULL,
	note TEXT
);

INSERT INTO contacts (last_name, first_name, middle_name, phone_number, note)
VALUES
('Skachkov', 'Yuriy', 'Alexandrovich', '+79625173462', 'Literally me'),
('Ivanov', 'Ivan', '', '+79999999999', 'Test subject');

