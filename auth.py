import streamlit as st
import hashlib
import hmac
import secrets
from db import connect_db


# Generate secure password hash
def hash_password(password):
    salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600000
    )

    return salt.hex(), password_hash.hex()


# Verify login credentials
def verify_user(username, password):

    conn = None
    cur = None

    try:
        conn = connect_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT salt, password_hash
            FROM users
            WHERE username = %s
        """, (username,))

        user = cur.fetchone()

        if user is None:
            return False

        salt = bytes.fromhex(user[0])

        entered_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            600000
        ).hex()

        return hmac.compare_digest(entered_hash, user[1])

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


# Protect individual pages
def require_login():

    if not st.session_state.get("logged_in", False):
        st.warning("Please login to access this page.")
        st.stop()