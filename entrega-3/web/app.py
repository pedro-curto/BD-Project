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
def products_index():
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                SELECT SKU, name, description, price, ean
                FROM product
                """
            )
            products = cur.fetchall()

    return render_template("products/index.html", products=products)


@app.route("/products/create", methods=["POST"])
def products_create():
    sku = request.form["sku"]
    name = request.form["name"]
    description = request.form["description"]
    price = request.form["price"]
    ean = request.form["ean"]

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO product (SKU, name, description, price, ean)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (sku, name, description, price, ean),
            )
            conn.commit()

    return redirect(url_for("products_index"))


@app.route("/products/<sku>/delete", methods=["POST"])
def products_delete(sku):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM product
                WHERE SKU = %s
                """,
                (sku,),
            )
            conn.commit()

    return redirect(url_for("products_index"))



@app.route("/products/<sku>/update", methods=["GET", "POST"])
def products_update(sku):
    """Update a product."""

    # Retrieve the product from the database
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            product = cur.execute(
                """
                SELECT sku, name, price, description
                FROM product
                WHERE sku = %(sku)s;
                """,
                {"sku": sku},
            ).fetchone()
            log.debug(f"Found {cur.rowcount} rows.")

    if request.method == "POST":
        # Retrieve updated information from the form
        name = request.form["name"]
        price = request.form["price"]
        description = request.form["description"]

        # Perform validation on the updated information
        error = None
        if not name:
            error = "Name is required."
        elif not price:
            error = "Price is required."
        elif not description:
            error = "Description is required."

        # If there are no validation errors, update the product in the database
        if error is None:
            with pool.connection() as conn:
                with conn.cursor(row_factory=namedtuple_row) as cur:
                    cur.execute(
                        """
                        UPDATE product
                        SET name = %(name)s, price = %(price)s, description = %(description)s
                        WHERE product_id = %(product_id)s;
                        """,
                        {
                            "product_id": product_id,
                            "name": name,
                            "price": price,
                            "description": description,
                        },
                    )
                conn.commit()
            return redirect(url_for("products_index"))

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
                """
            )
            suppliers = cur.fetchall()

    return render_template("suppliers/index.html", suppliers=suppliers)


@app.route("/suppliers/create", methods=["POST"])
def suppliers_create():
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


@app.route("/suppliers/<tin>/delete", methods=["POST"])
def suppliers_delete(tin):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM supplier
                WHERE TIN = %s
                """,
                (tin,),
            )
            conn.commit()

    return redirect(url_for("suppliers_index"))


# --- Clients ---
@app.route("/clients", methods=["GET"])
def clients_index():
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                SELECT cust_no, name, address
                FROM customer
                """
            )
            clients = cur.fetchall()

    return render_template("clients/index.html", clients=clients)


@app.route("/clients/create", methods=["POST"])
def clients_create():
    cust_no = request.form["cust_no"]
    name = request.form["name"]
    address = request.form["address"]

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO customer (cust_no, name, address)
                VALUES (%s, %s, %s)
                """,
                (cust_no, name, address),
            )
            conn.commit()

    return redirect(url_for("clients_index"))


@app.route("/clients/<cust_no>/delete", methods=["POST"])
def clients_delete(cust_no):
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM customer
                WHERE cust_no = %s
                """,
                (cust_no,),
            )
            conn.commit()

    return redirect(url_for("clients_index"))


# --- Orders and Payments ---
@app.route("/orders", methods=["GET"])
def orders_index():
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                SELECT order_no, cust_no, order_date, status
                FROM orders
                """
            )
            orders = cur.fetchall()

    return render_template("orders/index.html", orders=orders)


@app.route("/orders/create", methods=["POST"])
def orders_create():
    cust_no = request.form["cust_no"]
    order_date = request.form["order_date"]
    status = request.form["status"]

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO orders (cust_no, order_date, status)
                VALUES (%s, %s, %s)
                """,
                (cust_no, order_date, status),
            )
            conn.commit()

    return redirect(url_for("orders_index"))


@app.route("/payments", methods=["GET"])
def payments_index():
    with pool.connection() as conn:
        with conn.cursor(row_factory=namedtuple_row) as cur:
            cur.execute(
                """
                SELECT order_no, payment_date, amount
                FROM payment
                """
            )
            payments = cur.fetchall()

    return render_template("payments/index.html", payments=payments)


@app.route("/payments/create", methods=["POST"])
def payments_create():
    order_no = request.form["order_no"]
    payment_date = request.form["payment_date"]
    amount = request.form["amount"]

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO payment (order_no, payment_date, amount)
                VALUES (%s, %s, %s)
                """,
                (order_no, payment_date, amount),
            )
            conn.commit()

    return redirect(url_for("payments_index"))


@app.route("/ping", methods=("GET",))
def ping():
    log.debug("ping!")
    return jsonify({"message": "pong!", "status": "success"})


if __name__ == "__main__":
    app.run()
