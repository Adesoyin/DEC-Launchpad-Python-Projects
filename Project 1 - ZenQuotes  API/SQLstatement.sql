--Created the sample table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    email_address VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    firstname VARCHAR(50),
    subscription_status VARCHAR(10) CHECK (subscription_status IN ('Active', 'Inactive')),
    email_frequency_preference VARCHAR(10) CHECK (email_frequency_preference IN ('Daily', 'Weekly'))
);

-- Inserted 5 sample rows
INSERT INTO users (email_address, name, firstname, subscription_status, email_frequency_preference) VALUES
('adeboladesoyin@gmail.com', 'Adebola Adesoyin', 'Adebola', 'Active', 'Daily'),
('michael.brown@inboxbase.org', 'Michael Brown', 'Micheal', 'Inactive', 'Weekly'),
('lucy.smith@noreplydemo.com', 'Lucy Smith', 'Lucy', 'Active', 'Weekly'),
('dadebola.adesoyin@avonhealthcare.com', 'David Adams', 'David', 'Inactive', 'Daily'),
('emma.johnson@mailnode.org', 'Emma Johnson', 'Emma', 'Active', 'Weekly');

-- Verify the data
SELECT * FROM users;
