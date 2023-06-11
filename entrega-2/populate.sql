INSERT INTO Employee (ssn, tin, bdate, name) 
VALUES (111111111, 123123123, '2003-08-12', 'Empregado 1'),
       (222222222, 456456456, '2003-04-25', 'Empregado 2'),
       (333333333, 789789789, '2003-04-26', 'Empregado 3'),
       (444444444, 987987987, '2002-10-02', 'Empregado 4'),
       (555555555, 678678678, '2001-09-04', 'Empregado 5'),
       (666666666, 567567567, '2000-08-07', 'Empregado 6'),
       (777777777, 890890890, '1998-07-06', 'Empregado 7'),
       (888888888, 345345345, '1999-06-10', 'Empregado 8'),
       (999999999, 234234234, '1990-05-20', 'Empregado 9'); 

INSERT INTO Workplace(address, lat, long)
VALUES ('Morada Local Trabalho 1', 21.738, -78.019),
       ('Morada Local Trabalho 2', 09.883, 91.291),
       ('Morada Local Trabalho 3', 77.210, -32.009),
       ('Morada Local Trabalho 4', 44.444, 22.912),
       ('Morada Local Trabalho 5', -65.921, 33.092),
       ('Morada Local Trabalho 6', -03.123, -45.921),
       ('Morada Local Trabalho 7', 09.832, 12.092),
       ('Morada Local Trabalho 8', 33.212, -03.999),
       ('Morada Local Trabalho 9', 35.721, -98.112),
       ('Morada Local Trabalho 10', 22.111, -87.001),
       ('Morada Local Trabalho 11', -53.444, 12.111),
       ('Morada Local Trabalho 12', -29.212, -42.111);

INSERT INTO Department(name)
VALUES ('Operations'),
       ('IT'),
       ('Logistics'),
       ('Marketing'),
       ('Sales'),
       ('Finance'),
       ('HR'),
       ('Legal'),
       ('R&D');

INSERT INTO Works(ssn, address, name)
VALUES (111111111, 'Morada Local Trabalho 1', 'Operations'),
       (222222222, 'Morada Local Trabalho 2', 'Marketing'),
       (333333333, 'Morada Local Trabalho 12', 'IT'),
       (444444444, 'Morada Local Trabalho 4', 'Finance'),
       (555555555, 'Morada Local Trabalho 11', 'R&D'),
       (666666666, 'Morada Local Trabalho 6', 'HR'),
       (777777777, 'Morada Local Trabalho 7', 'IT'),
       (888888888, 'Morada Local Trabalho 8', 'Legal'),
       (999999999, 'Morada Local Trabalho 9', 'IT');

INSERT INTO Office(address)
VALUES ('Morada Local Trabalho 1'),
       ('Morada Local Trabalho 2'),
       ('Morada Local Trabalho 3'),
       ('Morada Local Trabalho 4'),
       ('Morada Local Trabalho 5'),
       ('Morada Local Trabalho 6');

INSERT INTO Warehouse(address)
VALUES ('Morada Local Trabalho 7'),
       ('Morada Local Trabalho 8'),
       ('Morada Local Trabalho 9'),
       ('Morada Local Trabalho 10'),
       ('Morada Local Trabalho 11'),
       ('Morada Local Trabalho 12');

INSERT INTO Product(sku, name, description, price)
VALUES (11122233, 'Produto 1', 'Descricao Produto 1', 5.49),
       (22233344, 'Produto 2', 'Descricao Produto 2', 10.79),
       (33344455, 'Produto 3', 'Descricao Produto 3', 199.98),
       (44455566, 'Produto 4', 'Descricao Produto 4', 0.99),
       (55566677, 'Produto 5', 'Descricao Produto 5', 3.98),
       (66677788, 'Produto 6', 'Descricao Produto 6', 4.49),
       (77788899, 'Produto 7', 'Descricao Produto 7', 59.99),
       (88899900, 'Produto 8', 'Descricao Produto 8', 299.99),
       (99900011, 'Produto 9', 'Descricao Produto 9', 1099.99);

INSERT INTO Supplier(tin, sku, name, address, date)
VALUES (987332121, 11122233, 'Nome Fornecedor 1', 'Endereço Fornecedor 1', '2020-01-01'),
       (999777532, 22233344, 'Nome Fornecedor 2', 'Endereço Fornecedor 2', '2023-01-06'),
       (111998212, 33344455, 'Nome Fornecedor 3', 'Endereço Fornecedor 3', '2022-04-29'),
       (987654321, 44455566, 'Nome Fornecedor 4', 'Endereço Fornecedor 4', '2021-02-28'),
       (987612341, 55566677, 'Nome Fornecedor 5', 'Endereço Fornecedor 5', '2020-03-01'),
       (123333333, 66677788, 'Nome Fornecedor 6', 'Endereço Fornecedor 6', '2020-03-01'),
       (123444444, 77788899, 'Nome Fornecedor 7', 'Endereço Fornecedor 7', '2020-03-01'),
       (123555555, 88899900, 'Nome Fornecedor 8', 'Endereço Fornecedor 8', '2020-03-01'),
       (123666666, 99900011, 'Nome Fornecedor 9', 'Endereço Fornecedor 9', '2020-03-01');

INSERT INTO EanProduct(sku, ean)
VALUES (11122233, 9876543219999),
       (22233344, 9876123412222),
       (33344455, 9876123413333),
       (44455566, 9876123414444),
       (55566677, 9876123415555),
       (66677788, 9876123416666),
       (77788899, 9876123417777);

INSERT INTO Delivery(address, sku, tin)
VALUES ('Morada Local Trabalho 1', 11122233, 111998212),
       ('Morada Local Trabalho 2', 22233344, 987332121),
       ('Morada Local Trabalho 3', 33344455, 987332121),
       ('Morada Local Trabalho 4', 44455566, 987332121),
       ('Morada Local Trabalho 5', 55566677, 987332121),
       ('Morada Local Trabalho 6', 66677788, 987332121),
       ('Morada Local Trabalho 7', 77788899, 987332121),
       ('Morada Local Trabalho 8', 88899900, 987332121),
       ('Morada Local Trabalho 9', 99900011, 987332121);

INSERT INTO Customer(cust_no, name, email, phone, address)
VALUES (1990, 'Nome Cliente 1', 'emailcliente1@hotmail.com', 919821223, 'Morada Cliente 1'),
       (1991, 'Nome Cliente 2', 'emailcliente2@gmail.com', 969988190, 'Morada Cliente 2'),
       (1992, 'Nome Cliente 3', 'emailcliente3@yahoo.com', 921006124, 'Morada Cliente 3'),
       (1993, 'Nome Cliente 4', 'emailcliente4@gmail.com', 919872193, 'Morada Cliente 4'),
       (1994, 'Nome Cliente 5', 'emailcliente5@gmail.com', 927168900, 'Morada Cliente 5'),
       (1995, 'Nome Cliente 6', 'emailcliente6@gmail.com', 912054123, 'Morada Cliente 6'),
       (1996, 'Nome Cliente 7', 'emailcliente7@gmail.com', 960183321, 'Morada Cliente 7'),
       (1997, 'Nome Cliente 8', 'emailcliente8@gmail.com', 915678212, 'Morada Cliente 8'),
       (1998, 'Nome Cliente 9', 'emailcliente9@gmail.com', 918345678, 'Morada Cliente 9');

INSERT INTO Orders(order_no, cust_no, date)
VALUES (1, 1990, '2021-05-25'),
       (2, 1990, '2021-05-27'),
       (3, 1992, '2023-01-21'),
       (4, 1991, '2021-07-03'),
       (5, 1993, '2020-03-20'),
       (6, 1994, '2022-01-10'),
       (7, 1995, '2023-02-02'),
       (8, 1996, '2023-01-31'),
       (9, 1997, '2021-09-15');

INSERT INTO Process(ssn, order_no)
VALUES (111111111, 1),
       (333333333, 2),
       (333333333, 3),
       (444444444, 9),
       (555555555, 7),
       (666666666, 6),
       (777777777, 8),
       (888888888, 4),
       (999999999, 5);

INSERT INTO Contains(order_no, sku, qty)
VALUES (1, 11122233, 10),
       (1, 22233344, 2),
       (1, 33344455, 7),
       (2, 22233344, 200),
       (3, 11122233, 1000),
       (3, 33344455, 5),
       (4, 44455566, 1),
       (4, 55566677, 2),
       (4, 66677788, 20),
       (5, 11122233, 7),
       (5, 66677788, 6),
       (6, 77788899, 21),
       (7, 77788899, 300),
       (7, 99900011, 100),
       (8, 55566677, 50),
       (8, 99900011, 300),
       (9, 11122233, 100),
       (9, 33344455, 200),
       (9, 88899900, 12);

INSERT INTO Sale (order_no, cust_no)
VALUES (1, 1990),
       (2, 1993),
       (3, 1992),
       (4, 1991),
       (7, 1995),
       (9, 1998);
