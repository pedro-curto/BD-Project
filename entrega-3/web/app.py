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
app.secret_key = "088ac63ff40dba3a745b6edd15a7ca55"
log = app.logger

# root goes to product_index -> landing page displays products
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
        # if ean is empty, we transform it to null not to cause an error
        if not ean:
            ean = None
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT sku
                    FROM product
                    WHERE sku = %(sku)s;
                    """,
                    {"sku": sku},
                )
                product_sku = cur.fetchone()
                if product_sku:
                    flash("SKU already exists! Please choose a new one.")
                    return redirect(url_for("create_product"))
                
                cur.execute(
                    """
                    INSERT INTO product (SKU, name, description, price, ean)
                    VALUES (%(sku)s, %(name)s, %(description)s, %(price)s, 
                    %(ean)s);
                    """,
                    {"sku": sku, "name": name, "description": description,
                     "price": price, "ean": ean}
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
                    WHERE sku = %(sku)s
                );
                """,
                {"sku": sku},
            )
            cur.execute(
                """
                DELETE FROM contains
                WHERE SKU = %(sku)s;
                """,
                {"sku": sku},
            )
            # TODO as communicated on slack, we can transform it to NULL
            cur.execute(
                """
                DELETE FROM supplier
                WHERE SKU = %(sku)s;
                """,
                {"sku": sku},
            )
            # now, we delete from the product table
            cur.execute(
                """
                DELETE FROM product
                WHERE SKU = %(sku)s;
                """,
                {"sku": sku},
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
                WHERE sku = %(sku)s;
                """,
                {"sku": sku},
                
            ).fetchone()
            log.debug(f"Found {cur.rowcount} rows.") #TODO remove? 

    if request.method == "POST":
        # Retrieve updated information from the form
        price = request.form["price"]
        description = request.form["description"]
        
        with pool.connection() as conn:
            with conn.cursor(row_factory=namedtuple_row) as cur:
                cur.execute(
                    """
                    UPDATE product
                    SET price = %(price)s, description = %(description)s
                    WHERE sku = %(sku)s;
                    """,
                    {"price": price, "description": description, 
                        "sku": sku},
                )
            conn.commit()
        return redirect(url_for("product_index"))
# case GET -> renders products/update.html
    else:
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
                    SELECT tin
                    FROM supplier
                    WHERE tin = %(tin)s;
                    """,
                    {"tin": tin},
                )
                supplier_tin = cur.fetchone()
                if supplier_tin:
                    flash("TIN already assigned to an existing supplier! \
                          Please choose a new one.")
                    return redirect(url_for("create_supplier"))
                
                cur.execute(
                    """
                    SELECT sku
                    FROM product
                    WHERE sku = %(sku)s;
                    """,
                    {"sku": sku},
                )
                product_sku = cur.fetchone()
                if not product_sku:
                    flash("SKU does not exist! Please choose an existing one.")
                    return redirect(url_for("create_supplier"))
                
                cur.execute(
                    """
                    INSERT INTO supplier (TIN, name, address, SKU, date)
                    VALUES (%(tin)s, %(name)s, %(address)s, %(sku)s, %(date)s);
                    """,
                    {"tin": tin, "name": name, "address": address, "sku": sku, 
                     "date": date},
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
                WHERE TIN = %(tin)s;
                """,
                {"tin": tin},
            )
            # then, delete from supplier table
            cur.execute(
                """
                DELETE FROM supplier
                WHERE TIN = %(tin)s;
                """,
                {"tin": tin},
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
                    VALUES(%(cust_no)s, %(name)s, %(email)s, %(phone)s, %(address)s));
                    """,
                    {"cust_no": cust_no, "name": name, "email": email, 
                     "phone": phone, "address": address}
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
                    WHERE cust_no = %(cust_no)s
                ); 
                """,
                {"cust_no": cust_no},    
            )
            # contains
            cur.execute(
                """
                DELETE FROM contains
                WHERE order_no IN(
                    SELECT order_no
                    FROM orders
                    WHERE cust_no = %(cust_no)s
                ); 
                """,
                {"cust_no": cust_no},   
            )
            # pay
            cur.execute(
                """
                DELETE FROM pay
                WHERE order_no IN (
                    SELECT order_no
                    FROM orders
                    WHERE cust_no = %(cust_no)s
                );
                """,
                {"cust_no": cust_no}, 
            )
            cur.execute(
                """
                DELETE FROM pay
                WHERE cust_no = %(cust_no)s;
                """,
                {"cust_no": cust_no},
            )
            # orders
            cur.execute(
                """
                DELETE FROM orders
                WHERE cust_no = %(cust_no)s;
                """,
                {"cust_no": cust_no},
            )
            # finally, delete from customer table
            cur.execute(
                """
                DELETE FROM customer
                WHERE cust_no = %(cust_no)s;
                """,
                {"cust_no": cust_no},
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
                ORDER BY order_no ASC;
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
    # case GET -> renders orders/create.html
    if request.method == "GET":
        # fetches all products to display them in the order creation page
        with pool.connection() as conn:
            with conn.cursor(row_factory=namedtuple_row) as cur:
                cur.execute(
                    """
                    SELECT name, description, price
                    FROM product;
                    """
                )
                products = cur.fetchall()
        return render_template("orders/create.html", products=products) 
    
    order_no = request.form["order_no"]
    cust_no = request.form["cust_no"]
    date = request.form["date"]     
        
    with pool.connection() as conn:
        with conn.cursor() as cur:
            # checks if the customer placing the order exists
            cur.execute(
                """
                SELECT cust_no
                FROM customer
                WHERE cust_no = %(cust_no)s;
                """,
                {"cust_no": cust_no},
            )
            customer_number = cur.fetchone()
            if not customer_number:
                flash("Customer not found! Please insert an existing \
                        customer number.")
                return redirect(url_for("create_order"))
            
            # inserts the order info to the orders table
            cur.execute(
                """
                INSERT INTO orders (order_no, cust_no, date)
                VALUES(%(order_no)s, %(cust_no)s, %(date)s);
                """,
                {"order_no": order_no, "cust_no": cust_no, "date": date},
            )
            
            # inserts all products that the order contains in the "contains" table
            # fetches all products from the form
            products = request.form.getlist("products")
            
            for product in products:
                sku = product.sku
                qty = product.quantity
                if int(qty) > 0:
                    cur.execute(
                        """ 
                        INSERT INTO contains (order_no, sku, qty)
                        VALUES(%(order_no)s, %(sku)s, %(qty)s);
                        """,
                        {"order_no": order_no, "sku": sku, "qty": qty},
                    )                    
                        
            # finally, checks if the order has been paid: if so, adds to "pay"
            pay_option = request.form["pay_optn"]
            if pay_option == "now":
                cur.execute(
                    """
                    INSERT INTO pay (order_no, cust_no)
                    VALUES(%(order_no)s, %(cust_no)s);
                    """,
                    {"order_no": order_no, "cust_no": cust_no},
                )
    return redirect(url_for("orders_index"))
    


@app.route("/orders/<order_no>/pay", methods=["GET", "POST"])
def pay_order(order_no):
    if request.method == "POST":
        cust_no = request.form["cust_no"]
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT * 
                    FROM customer
                    WHERE cust_no = %(cust_no)s;
                    """,
                    {"cust_no": cust_no},
                ) 
                customer = cur.fetchone()
                if customer:
                    # adds to pay table
                    cur.execute(
                        """
                        INSERT INTO pay (order_no, cust_no)
                        VALUES(%(order_no)s, %(cust_no)s);
                        """,
                        {"order_no": order_no, "cust_no": cust_no},
                    )
                    conn.commit()
                
                    flash("Payment successful!", "success")
                    return redirect(url_for("orders_index"))
                else:
                    flash("Customer not found!", "danger")
                    return redirect(url_for("pay_order", order_no=order_no))
    # case GET -> fetches parameters and renders orders/pay.html
    else:
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    # gets order price
                    """
                    SELECT SUM(price*qty) AS order_price
                    FROM orders AS o
                    JOIN contains USING(order_no)
                    JOIN product USING(sku)
                    WHERE o.order_no = %(order_no)s;
                    """,
                    {"order_no": order_no},
                )
                order_price = cur.fetchone()[0]
                
                # gets order info
                cur.execute(
                    """
                    SELECT *
                    FROM orders
                    WHERE order_no = %(order_no)s;
                    """,
                    {"order_no": order_no},
                )
                order = cur.fetchone()
        
        return render_template("orders/pay.html", order_no=order_no, 
                               order=order, order_price=order_price)



@app.route("/ping", methods=("GET",))
def ping():
    log.debug("ping!")
    return jsonify({"message": "pong!", "status": "success"})


if __name__ == "__main__":
    app.run()



# products/upadate.html before end
# <form action="{{ url_for('product_index', sku=product['sku']) }}" method="post">
#     <input type="hidden" name="_method" value="DELETE">
#     <input type="hidden" name="sku" value="{{ product['sku'] }}">
#     <input class="danger" type="submit" value="Delete" onclick="return confirm('Are you sure?');">
#   </form>