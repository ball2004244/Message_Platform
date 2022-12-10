CREATE DATABASE IF NOT EXISTS test_database;

CREATE TABLE IF NOT EXISTS test_database.customer (
	ID int,
    CustomerName varchar(255),
    Address varchar(255)
);

SELECT * FROM test_database.customer;
INSERT INTO test_database.customer (ID, CustomerName, Address) VALUE ('1', 'Tam', 'Tampa');

-- DROP DATABASE IF EXISTS test_database;
-- TRUNCATE TABLE test_database.customer;
-- DROP TABLE IF EXISTS test_database.customer;