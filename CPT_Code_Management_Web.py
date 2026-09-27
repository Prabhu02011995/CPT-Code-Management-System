from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)


# PostgreSQL connection
def get_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="cpt_management",
        user="postgres",
        password="Postgre@123",
        port="5432"
    )
    return connection


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Add CPT Code
@app.route("/add", methods=["GET", "POST"])
def add_cpt_code():

    if request.method == "POST":

        cpt_id = int(request.form["id"])
        cpt_code = request.form["cpt_code"]
        procedure_name = request.form["procedure_name"]
        description = request.form["description"]
        category = request.form["category"]
        fee = float(request.form["fee"])
        status = request.form["status"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO cpt_codes
            (id, cpt_code, procedure_name, description, category, fee, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                cpt_id,
                cpt_code,
                procedure_name,
                description,
                category,
                fee,
                status
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return "CPT Code added successfully!"

    return render_template("add.html")


# View CPT Codes
@app.route("/view")
def view_cpt_codes():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM cpt_codes")

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("view.html", rows=rows)


# Search CPT Code
@app.route("/search", methods=["GET", "POST"])
def search_cpt_code():

    row = None
    searched = False

    if request.method == "POST":

        cpt_code = request.form["cpt_code"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM cpt_codes WHERE cpt_code = %s",
            (cpt_code,)
        )

        row = cursor.fetchone()

        cursor.close()
        connection.close()

        searched = True

    return render_template(
        "search.html",
        row=row,
        searched=searched
    )


# Update CPT Code
@app.route("/update", methods=["GET", "POST"])
def update_cpt_code():

    if request.method == "POST":

        cpt_code = request.form["cpt_code"]
        procedure_name = request.form["procedure_name"]
        description = request.form["description"]
        category = request.form["category"]
        fee = float(request.form["fee"])
        status = request.form["status"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE cpt_codes
            SET procedure_name = %s,
                description = %s,
                category = %s,
                fee = %s,
                status = %s
            WHERE cpt_code = %s
            """,
            (
                procedure_name,
                description,
                category,
                fee,
                status,
                cpt_code
            )
        )

        connection.commit()

        if cursor.rowcount > 0:
            message = "CPT Code updated successfully!"
        else:
            message = "CPT Code not found."

        cursor.close()
        connection.close()

        return message

    return render_template("update.html")


# Delete CPT Code
@app.route("/delete", methods=["GET", "POST"])
def delete_cpt_code():

    if request.method == "POST":

        cpt_code = request.form["cpt_code"]

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM cpt_codes WHERE cpt_code = %s",
            (cpt_code,)
        )

        connection.commit()

        if cursor.rowcount > 0:
            message = "CPT Code deleted successfully!"
        else:
            message = "CPT Code not found."

        cursor.close()
        connection.close()

        return message

    return render_template("delete.html")


# Start Flask
if __name__ == "__main__":
    app.run(debug=True)