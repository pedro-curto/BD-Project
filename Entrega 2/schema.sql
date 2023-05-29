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
    name VARCHAR(80),
    CHECK (ssn > 0 AND tin > 0)
    /* IC-4: Any ssn in Employee must exist in works. This means that any ssn 
    value existing in this table must be present in the works table. */
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
    address VARCHAR(80) PRIMARY KEY REFERENCES workplace ON DELETE CASCADE
);

CREATE TABLE warehouse(
    address VARCHAR(80) PRIMARY KEY REFERENCES workplace ON DELETE CASCADE
);

CREATE TABLE product(
    sku VARCHAR(16) PRIMARY KEY,
    name VARCHAR(80),
    description VARCHAR(80),
    price NUMERIC(10, 2),
    CHECK (price > 0)
    /* IC-5: Any sku in Product must exist in Supplier. This means that any 
    sku value existing in this table must be present in the supplier table. */
);

CREATE TABLE supplier(
    tin NUMERIC(9) PRIMARY KEY,
    sku VARCHAR(16) NOT NULL REFERENCES product,
    name VARCHAR(80),
    address VARCHAR(80),
    date DATE,
    CHECK (tin > 0)
);

CREATE TABLE eanProduct(
    sku VARCHAR(16) PRIMARY KEY REFERENCES product ON DELETE CASCADE, 
    ean NUMERIC(13),
    CHECK (ean > 0)
);

CREATE TABLE delivery(
    address VARCHAR(80) REFERENCES workplace,
    sku VARCHAR(16) REFERENCES product, 
    tin NUMERIC(9) REFERENCES supplier, 
    PRIMARY KEY (address, sku, tin)
);

CREATE TABLE customer(
    cust_no SERIAL PRIMARY KEY,
    name VARCHAR(80),
    email VARCHAR(80) UNIQUE,
    phone NUMERIC(12),
    address VARCHAR(80),
    CHECK (phone > 0)
);

CREATE TABLE orders(
    order_no SERIAL PRIMARY KEY, 
    cust_no SERIAL NOT NULL REFERENCES customer,
    date DATE
    /* IC-6: Any order_no in Order must exist in contains. This means that any 
    order_no value existing in this table must be present in the 
    contains table. */
);


CREATE TABLE process(
    ssn NUMERIC(11) REFERENCES employee,
    order_no SERIAL REFERENCES orders,
    PRIMARY KEY (ssn, order_no)
);

CREATE TABLE contains(
    order_no SERIAL REFERENCES orders,
    sku VARCHAR(16) REFERENCES product,
    qty NUMERIC(20),
    PRIMARY KEY (order_no, sku),
    CHECK (qty > 0)
);

CREATE TABLE sale(
    order_no SERIAL PRIMARY KEY REFERENCES orders ON DELETE CASCADE,
    cust_no SERIAL NOT NULL REFERENCES customer
    /* IC-7: Customers can only pay for the Sale of an Order they have placed 
    themselves. This implies that all cust_no in sale must be the same as the 
    cust_no associated with the order_no in the Orders table. */
); 
