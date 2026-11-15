from db import connect_db
from auth import hash_password
from getpass import getpass

username = input("Enter username: ").strip()
password = getpass("Enter password: ")
confirm_password = getpass("Confirm password: ")

if not username:
    print("Username cannot be empty.")

elif len(password) < 8:
    print("Password must contain at least 8 characters.")

elif password != confirm_password:
    print("Passwords do not match.")

else:
    conn = None
    cur = None

    try:
        salt, password_hash = hash_password(password)

        conn = connect_db()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO users
            (username, password_hash, salt)
            VALUES (%s, %s, %s)
        """, (username, password_hash, salt))

        conn.commit()

        print("User created successfully!")

    except Exception as e:
        if conn:
            conn.rollback()

        print("Error:", e)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()