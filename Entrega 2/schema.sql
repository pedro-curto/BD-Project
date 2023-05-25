DROP TABLE employee, workplace, department, works, office, warehouse, product, supplier, eanProduct, delivery, customer, orders, process, contains, sale;

CREATE TABLE IF NOT EXISTS employee(
    ssn NUMERIC(12) PRIMARY KEY,
    tin NUMERIC(12) UNIQUE,
    bdate DATE,
    name VARCHAR(80)
);

CREATE TABLE IF NOT EXISTS workplace(
    address VARCHAR(80) PRIMARY KEY,
    lat FLOAT,
    long FLOAT,
    UNIQUE(lat, long)
);

CREATE TABLE IF NOT EXISTS department(
    name VARCHAR(80) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS works(
    ssn NUMERIC(12) REFERENCES employee,
    address VARCHAR(80) REFERENCES workplace,
    name VARCHAR(80) REFERENCES department,
    PRIMARY KEY (ssn, address, name)
);

CREATE TABLE IF NOT EXISTS office(
    address VARCHAR(80) PRIMARY KEY,
    FOREIGN KEY (address) REFERENCES workplace (address)
);

CREATE TABLE IF NOT EXISTS warehouse(
    address VARCHAR(80) PRIMARY KEY,
    FOREIGN KEY (address) REFERENCES workplace (address)
);

CREATE TABLE IF NOT EXISTS product(
    sku NUMERIC(8) PRIMARY KEY,
    name VARCHAR(80),
    description VARCHAR(80),
    price FLOAT
);

CREATE TABLE IF NOT EXISTS supplier(
    tin NUMERIC(12) PRIMARY KEY,
    sku NUMERIC(8) NOT NULL REFERENCES product,
    name VARCHAR(80),
    address VARCHAR(80),
    date DATE
);

CREATE TABLE IF NOT EXISTS eanProduct(
    sku NUMERIC(8) PRIMARY KEY,
    ean NUMERIC(13)
);

CREATE TABLE IF NOT EXISTS delivery(
    address VARCHAR(80) REFERENCES workplace,
    sku NUMERIC(8) REFERENCES product, 
    tin NUMERIC(12) REFERENCES supplier, 
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
    ssn NUMERIC(12) REFERENCES employee,
    order_no NUMERIC(20) REFERENCES orders,
    PRIMARY KEY (ssn, order_no)
);

CREATE TABLE IF NOT EXISTS contains(
    order_no NUMERIC(20) REFERENCES orders,
    sku NUMERIC(8) REFERENCES product,
    qty NUMERIC(20),
    PRIMARY KEY (order_no, sku)
);

CREATE TABLE IF NOT EXISTS sale(
    order_no NUMERIC(20) PRIMARY KEY REFERENCES orders,
    cust_no NUMERIC(20) NOT NULL REFERENCES customer
); 
