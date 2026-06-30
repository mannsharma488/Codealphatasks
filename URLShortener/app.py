from flask import Flask, request, jsonify, redirect, render_template
import sqlite3
import random
import string

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        short_code TEXT UNIQUE,
        long_url TEXT,
        clicks INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

init_db()


# Home Page
@app.route("/")
def home():
    return render_template("index.html")


# URL Shortener API
@app.route("/shorten", methods=["POST"])
def shorten_url():

    data = request.get_json()

    long_url = data.get("url")
    custom_code = data.get("custom_code")

    if not long_url:
        return jsonify({"error": "URL is required"}), 400

    if not (
        long_url.startswith("http://")
        or long_url.startswith("https://")
    ):
        return jsonify({"error": "Invalid URL"}), 400

    if custom_code:
        short_code = custom_code
    else:
        short_code = ''.join(
            random.choices(
                string.ascii_letters + string.digits,
                k=6
            )
        )

    conn = sqlite3.connect("urls.db")
    cursor = conn.cursor()

    try:

        cursor.execute(
            "INSERT INTO urls(short_code,long_url) VALUES(?,?)",
            (short_code,long_url)
        )

        conn.commit()

    except sqlite3.IntegrityError:

        conn.close()

        return jsonify({
            "error":"Short code already exists"
        }),400

    conn.close()

    return jsonify({

        "short_code":short_code,

        "short_url":
        f"http://127.0.0.1:5000/{short_code}"

    })


# Redirect Route
@app.route("/<code>")
def redirect_url(code):

    conn=sqlite3.connect("urls.db")

    cursor=conn.cursor()

    cursor.execute(
        "SELECT long_url FROM urls WHERE short_code=?",
        (code,)
    )

    result=cursor.fetchone()

    if result:

        cursor.execute(
            "UPDATE urls SET clicks=clicks+1 WHERE short_code=?",
            (code,)
        )

        conn.commit()

        conn.close()

        return redirect(result[0])

    conn.close()

    return "Invalid URL"


# Analytics
@app.route("/analytics/<code>")
def analytics(code):

    conn=sqlite3.connect("urls.db")

    cursor=conn.cursor()

    cursor.execute(

        "SELECT long_url,clicks FROM urls WHERE short_code=?",

        (code,)

    )

    result=cursor.fetchone()

    conn.close()

    if result:

        return jsonify({

            "url":result[0],

            "clicks":result[1]

        })

    return jsonify({

        "error":"Short code not found"

    }),404


if __name__=="__main__":
    app.run(debug=True)