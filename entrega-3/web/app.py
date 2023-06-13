#!/usr/bin/python3
from logging.config import dictConfig

import psycopg
from flask import flash
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from psycopg.rows import namedtuple_row
from psycopg_pool import ConnectionPool


# postgres://{user}:{password}@{hostname}:{port}/{database-name}
DATABASE_URL = "postgres://db:db@postgres/db"

pool = ConnectionPool(conninfo=DATABASE_URL)
# the pool starts connecting immediately.

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s:%(lineno)s - %(funcName)20s(): %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)
log = app.logger


@app.route("/", methods=("GET",))

#---------------------------------- PRODUCTS ----------------------------------#

@app.route("/products", methods=["GET"])
def product_index():
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                SELECT sku, name, description, price, ean
                FROM product
                ORDER BY name ASC;
                """
            )
            products = cur.fetchall()

    return render_template("products/index.html", products=products)


@app.route("/products/create", methods=["GET", "POST"])
def create_product():
    if request.method == "POST":
        sku = request.form["sku"]
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        ean = request.form["ean_number"]
        if not ean:
            ean = None

        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO product (SKU, name, description, price, ean)
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (sku, name, description, price, ean),
                )
                conn.commit()

        return redirect(url_for("product_index"))
    # in case it is a GET request, we simply render the 'create.html' file
    else:
        return render_template("products/create.html")


@app.route("/products/<sku>/delete", methods=["POST"])
def delete_product(sku):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            # we need to delete the product from the dependent tables first
            cur.execute(
                """
                DELETE FROM delivery
                WHERE tin IN (
                    SELECT tin
                    FROM supplier
                    WHERE sku = %s
                );
                """,
                (sku,),
            )
            cur.execute(
                """
                DELETE FROM contains
                WHERE SKU = %s;
                """,
                (sku,),
            )
            # as communicated on slack, we can transform it to 
            cur.execute(
                """
                DELETE FROM supplier
                WHERE SKU = %s;
                """,
                (sku,),
            )
            # now, we delete from the product table
            cur.execute(
                """
                DELETE FROM product
                WHERE SKU = %s;
                """,
                (sku,),
            )
            conn.commit()

    return redirect(url_for("product_index"))



@app.route("/products/<sku>/update", methods=["GET", "POST"])
def update_product(sku):
    """Update a product."""
    # Retrieve the product from the database
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            product = cur.execute(
                """
                SELECT sku, name, price, description, ean
                FROM product
                WHERE sku = %s;
                """,
                (sku,),
            ).fetchone()
            log.debug(f"Found {cur.rowcount} rows.")

    if request.method == "POST":
        # Retrieve updated information from the form
        price = request.form["price"]
        description = request.form["description"]
        # Perform validation on the updated information
        error = False
        if not price:
            error = "Price is required."
        elif not description:
            error = "Description is required."

        # If there are no validation errors, update the product in the database
        if not error:
            with pool.connection() as conn:
                with conn.cursor(row_factory=namedtuple_row) as cur:
                    cur.execute(
                        """
                        UPDATE product
                        SET price = %s, description = %s
                        WHERE sku = %s;
                        """,
                        (price, description, sku),
                    )
                conn.commit()
            return redirect(url_for("product_index"))
        flash(error)

    return render_template("products/update.html", product=product)


#--------------------------------- SUPPLIERS ----------------------------------#

@app.route("/suppliers", methods=["GET"])
def suppliers_index():
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                SELECT TIN, name, address, SKU, date
                FROM supplier
                ORDER BY name ASC;
                """
            )
            suppliers = cur.fetchall()

    return render_template("suppliers/index.html", suppliers=suppliers)



@app.route("/suppliers/create", methods=["GET", "POST"])
def create_supplier():
    if request.method == "POST":
        tin = request.form["tin"]
        name = request.form["name"]
        address = request.form["address"]
        sku = request.form["sku"]
        date = request.form["date"]

        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO supplier (TIN, name, address, SKU, date)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (tin, name, address, sku, date),
                )
                conn.commit()

        return redirect(url_for("suppliers_index"))
    # in case it is a GET request, we simply render the 'create.html' file
    else:
        return render_template("suppliers/create.html")



@app.route("/suppliers/<tin>/delete", methods=["POST"])
def delete_supplier(tin):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            # delete from dependent table delivery first
            cur.execute(
                """
                DELETE FROM delivery
                WHERE TIN = %s;
                """,
                (tin,),
            )
            # then, delete from supplier table
            cur.execute(
                """
                DELETE FROM supplier
                WHERE TIN = %s;
                """,
                (tin,),
            )
            conn.commit()

    return redirect(url_for("suppliers_index"))


#---------------------------------- CUSTOMERS ---------------------------------#

@app.route("/customers", methods=["GET"])
def customers_index():
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                SELECT cust_no, name, email, phone ,address 
                FROM customer
                ORDER BY name ASC;
                """
            )
            customers = cur.fetchall()

    return render_template("customers/index.html", customers=customers)



@app.route("/customers/create", methods=["GET", "POST"])
def create_customer():
    if request.method == "POST":
        cust_no = request.form["cust_no"]
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        address = request.form["address"]
        
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO customer (cust_no, name, email, phone, address)
                    VALUES(%s, %s, %s, %s, %s);
                    """,
                    (cust_no, name, email, phone, address),
                )
                conn.commit()
                
        return redirect(url_for("customers_index"))
    # case GET -> renders create.html
    else:
        return render_template("customers/create.html")
    


@app.route("/customers/<cust_no>/delete", methods=["POST"])
def delete_customer(cust_no):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            # delete orders with associated cust_no first
            # process
            cur.execute(
                """
                DELETE FROM process
                WHERE order_no IN(
                    SELECT order_no
                    FROM orders
                    WHERE cust_no = %s
                ); 
                """,
                (cust_no,),    
            )
            # contains
            cur.execute(
                """
                DELETE FROM contains
                WHERE order_no IN(
                    SELECT order_no
                    FROM orders
                    WHERE cust_no = %s
                ); 
                """,
                (cust_no,),    
            )
            # pay
            cur.execute(
                """
                DELETE FROM pay
                WHERE order_no IN (
                    SELECT order_no
                    FROM orders
                    WHERE cust_no = %s
                );
                """,
                (cust_no,),
            )
            cur.execute(
                """
                DELETE FROM pay
                WHERE cust_no = %s;
                """,
                (cust_no,),
            )
            # orders
            cur.execute(
                """
                DELETE FROM orders
                WHERE cust_no = %s;
                """,
                (cust_no,),
            )
            # finally, delete from customer table
            cur.execute(
                """
                DELETE FROM customer
                WHERE cust_no = %s;
                """,
                (cust_no,),
            )

        conn.commit()

    return redirect(url_for("customers_index"))




#----------------------------------- ORDERS -----------------------------------#

@app.route("/orders", methods=["GET"])
def orders_index():
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                SELECT order_no, cust_no, date
                FROM orders
                ORDER BY date ASC;
                """
            )
            orders = cur.fetchall()
            # selects orders that haven't been paid to display the Pay button
            # only in those orders, in the orders/index.html file
            cur.execute(
                """
                SELECT order_no
                FROM orders
                WHERE order_no NOT IN(
                    SELECT order_no FROM pay
                );
                """
            )
            unpaid_orders = [row[0] for row in cur.fetchall()]

    return render_template("orders/index.html", orders=orders, unpaid_orders=unpaid_orders)


@app.route("/orders/create", methods=["GET", "POST"])
def create_order():
    if request.method == "POST":
        order_no = request.form["order_no"]
        cust_no = request.form["cust_no"]
        date = request.form["date"]     
           
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO customer (order_no, cust_no, date)
                    VALUES(%s, %s, %s);
                    """,
                    (order_no, cust_no, date),
                )
                conn.commit()
                
        return redirect(url_for("orders_index"))
    # case GET -> renders orders/create.html
    else:
        return render_template("orders/create.html")


@app.route("/orders/<order_no>/pay", methods=["GET", "POST"])
def pay_order():
    customer_no = request.form["customer_no"]

    # Check if the customer number exists in the database
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM customer WHERE cust_no = %s", (customer_no,))
            customer = cur.fetchone()

        if customer:
            flash("Payment successful!", "success")
        else:
            flash("Customer number not found!", "danger")
        
    return redirect(url_for("orders_index"))    



@app.route("/ping", methods=("GET",))
def ping():
    log.debug("ping!")
    return jsonify({"message": "pong!", "status": "success"})


if __name__ == "__main__":
    app.run()
