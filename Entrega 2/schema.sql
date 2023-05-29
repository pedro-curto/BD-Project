DROP TABLE IF EXISTS employee cascade;
DROP TABLE IF EXISTS workplace cascade;
DROP TABLE IF EXISTS department cascade;
DROP TABLE IF EXISTS works cascade;
DROP TABLE IF EXISTS office cascade;
DROP TABLE IF EXISTS warehouse cascade;
DROP TABLE IF EXISTS product cascade;
DROP TABLE IF EXISTS supplier cascade;
DROP TABLE IF EXISTS eanProduct cascade; 
DROP TABLE IF EXISTS delivery cascade;
DROP TABLE IF EXISTS customer cascade;
DROP TABLE IF EXISTS orders cascade;
DROP TABLE IF EXISTS process cascade;
DROP TABLE IF EXISTS contains cascade;
DROP TABLE IF EXISTS sale cascade;

CREATE TABLE employee(
    ssn NUMERIC(11) PRIMARY KEY,
    tin NUMERIC(9) UNIQUE,
    bdate DATE,
    name VARCHAR(80)
);

CREATE TABLE workplace(
    address VARCHAR(80) PRIMARY KEY,
    lat NUMERIC(5,2),
    long NUMERIC(5,2),
    UNIQUE(lat, long)
);

CREATE TABLE department(
    name VARCHAR(80) PRIMARY KEY
);

CREATE TABLE works(
    ssn NUMERIC(11) REFERENCES employee,
    address VARCHAR(80) REFERENCES workplace,
    name VARCHAR(80) REFERENCES department,
    PRIMARY KEY (ssn, address, name)
);

CREATE TABLE office(
    address VARCHAR(80) PRIMARY KEY REFERENCES workplace
);

CREATE TABLE warehouse(
    address VARCHAR(80) PRIMARY KEY REFERENCES workplace
);

CREATE TABLE product(
    sku VARCHAR(16) PRIMARY KEY,
    name VARCHAR(80),
    description VARCHAR(80),
    price NUMERIC(10, 2)
);

CREATE TABLE supplier(
    tin NUMERIC(9) PRIMARY KEY,
    sku VARCHAR(16) NOT NULL REFERENCES product,
    name VARCHAR(80),
    address VARCHAR(80),
    date DATE
);

CREATE TABLE eanProduct(
    sku VARCHAR(16) PRIMARY KEY,
    ean NUMERIC(13)
);

CREATE TABLE delivery(
    address VARCHAR(80) REFERENCES workplace,
    sku VARCHAR(16) REFERENCES product, 
    tin NUMERIC(9) REFERENCES supplier, 
    PRIMARY KEY (address, sku, tin)
);

CREATE TABLE customer(
    cust_no NUMERIC(20) PRIMARY KEY,
    name VARCHAR(80),
    email VARCHAR(80) UNIQUE,
    phone NUMERIC(12),
    address VARCHAR(80)
);

CREATE TABLE orders(
    order_no NUMERIC(20) PRIMARY KEY, 
    cust_no NUMERIC(20) NOT NULL REFERENCES customer,
    date DATE
);


CREATE TABLE process(
    ssn NUMERIC(11) REFERENCES employee,
    order_no NUMERIC(20) REFERENCES orders,
    PRIMARY KEY (ssn, order_no)
);

CREATE TABLE contains(
    order_no NUMERIC(20) REFERENCES orders,
    sku VARCHAR(16) REFERENCES product,
    qty NUMERIC(20),
    PRIMARY KEY (order_no, sku)
);

CREATE TABLE sale(
    order_no NUMERIC(20) PRIMARY KEY REFERENCES orders,
    cust_no NUMERIC(20) NOT NULL REFERENCES customer
); 
