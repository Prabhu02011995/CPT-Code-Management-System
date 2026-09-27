import psycopg2


# -----------------------------
# Database Connection
# -----------------------------
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="cpt_management",
        user="postgres",
        password="YOUR_PASSWORD",
        port="5432"
    )


# -----------------------------
# 1. Add CPT Code
# -----------------------------
def add_cpt_code():
    connection = get_connection()
    cursor = connection.cursor()

    cpt_id = int(input("Enter ID: "))
    cpt_code = input("Enter CPT code: ")
    procedure_name = input("Enter procedure name: ")
    description = input("Enter description: ")
    category = input("Enter category: ")
    fee = float(input("Enter fee: "))
    status = input("Enter status: ")

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

    print("CPT code added successfully!")

    cursor.close()
    connection.close()


# -----------------------------
# 2. View All CPT Codes
# -----------------------------
def view_all_cpt_codes():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM cpt_codes")

    rows = cursor.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No CPT records found.")

    cursor.close()
    connection.close()


# -----------------------------
# 3. Search CPT Code
# -----------------------------
def search_cpt_code():
    connection = get_connection()
    cursor = connection.cursor()

    cpt_code = input("Enter CPT code to search: ")

    cursor.execute(
        "SELECT * FROM cpt_codes WHERE cpt_code = %s",
        (cpt_code,)
    )

    rows = cursor.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("CPT code not found.")

    cursor.close()
    connection.close()


# -----------------------------
# 4. Update CPT Code
# -----------------------------
def update_cpt_code():
    connection = get_connection()
    cursor = connection.cursor()

    cpt_code = input("Enter CPT code to update: ")
    new_fee = float(input("Enter new fee: "))

    cursor.execute(
        """
        UPDATE cpt_codes
        SET fee = %s
        WHERE cpt_code = %s
        """,
        (new_fee, cpt_code)
    )

    connection.commit()

    if cursor.rowcount > 0:
        print("CPT code updated successfully!")
    else:
        print("CPT code not found.")

    cursor.close()
    connection.close()


# -----------------------------
# 5. Delete CPT Code
# -----------------------------
def delete_cpt_code():
    connection = get_connection()
    cursor = connection.cursor()

    cpt_code = input("Enter CPT code to delete: ")

    cursor.execute(
        "DELETE FROM cpt_codes WHERE cpt_code = %s",
        (cpt_code,)
    )

    connection.commit()

    if cursor.rowcount > 0:
        print("CPT code deleted successfully!")
    else:
        print("CPT code not found.")

    cursor.close()
    connection.close()


# -----------------------------
# Main Menu
# -----------------------------
def main_menu():

    while True:

        print("\n========================================")
        print("      CPT CODE MANAGEMENT SYSTEM")
        print("========================================")
        print("1. Add CPT Code")
        print("2. View All CPT Codes")
        print("3. Search CPT Code")
        print("4. Update CPT Code")
        print("5. Delete CPT Code")
        print("6. Exit")
        print("========================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_cpt_code()

        elif choice == "2":
            view_all_cpt_codes()

        elif choice == "3":
            search_cpt_code()

        elif choice == "4":
            update_cpt_code()

        elif choice == "5":
            delete_cpt_code()

        elif choice == "6":
            print("Thank you for using the system!")
            break

        else:
            print("Invalid choice. Please try again.")


# -----------------------------
# Start Program
# -----------------------------
main_menu()