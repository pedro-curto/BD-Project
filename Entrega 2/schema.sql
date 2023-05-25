DROP TABLE employee, workplace, department, works, office, warehouse, product, supplier, eanProduct, delivery, customer, orders, process, contains, sale;

CREATE TABLE IF NOT EXISTS employee(
    ssn NUMERIC(11) PRIMARY KEY,
    tin NUMERIC(9) UNIQUE,
    bdate DATE,
    name VARCHAR(80)
);

CREATE TABLE IF NOT EXISTS workplace(
    address VARCHAR(80) PRIMARY KEY,
    lat NUMERIC(5, 2),
    long NUMERIC(5, 2), 
    UNIQUE(lat, long)
);

CREATE TABLE IF NOT EXISTS department(
    name VARCHAR(80) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS works(
    ssn NUMERIC(11) REFERENCES employee,
    address VARCHAR(80) REFERENCES workplace,
    name VARCHAR(80) REFERENCES department,
    PRIMARY KEY (ssn, address, name)
);

CREATE TABLE IF NOT EXISTS office(
    address VARCHAR(80) PRIMARY KEY REFERENCES workplace
);

CREATE TABLE IF NOT EXISTS warehouse(
    address VARCHAR(80) PRIMARY KEY REFERENCES workplace
);

CREATE TABLE IF NOT EXISTS product(
    sku VARCHAR(12) PRIMARY KEY,
    name VARCHAR(80),
    description VARCHAR(80),
    price NUMERIC(10, 2)
);

CREATE TABLE IF NOT EXISTS supplier(
    tin NUMERIC(9) PRIMARY KEY,
    sku VARCHAR(12) NOT NULL REFERENCES product,
    name VARCHAR(80),
    address VARCHAR(80),
    date DATE
);

CREATE TABLE IF NOT EXISTS eanProduct(
    sku VARCHAR(12) PRIMARY KEY,
    ean NUMERIC(13)
);

CREATE TABLE IF NOT EXISTS delivery(
    address VARCHAR(80) REFERENCES workplace,
    sku VARCHAR(12) REFERENCES product, 
    tin NUMERIC(9) REFERENCES supplier, 
    PRIMARY KEY (address, sku, tin)
);

CREATE TABLE IF NOT EXISTS customer(
    cust_no NUMERIC(20) PRIMARY KEY,
    name VARCHAR(80),
    email VARCHAR(80) UNIQUE,
    phone NUMERIC(12),
    address VARCHAR(80)
);

CREATE TABLE IF NOT EXISTS orders(
    order_no NUMERIC(20) PRIMARY KEY, 
    cust_no NUMERIC(20) NOT NULL REFERENCES customer,
    date DATE
);


CREATE TABLE IF NOT EXISTS process(
    ssn NUMERIC(11) REFERENCES employee,
    order_no NUMERIC(20) REFERENCES orders,
    PRIMARY KEY (ssn, order_no)
);

CREATE TABLE IF NOT EXISTS contains(
    order_no NUMERIC(20) REFERENCES orders,
    sku VARCHAR(12) REFERENCES product,
    qty NUMERIC(20),
    PRIMARY KEY (order_no, sku)
);

CREATE TABLE IF NOT EXISTS sale(
    order_no NUMERIC(20) PRIMARY KEY REFERENCES orders,
    cust_no NUMERIC(20) NOT NULL REFERENCES customer
); 
