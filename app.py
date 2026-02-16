
import sqlite3
import os
from flask import Flask, render_template, request, redirect
app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# -------- DATABASE CREATE --------
def init_db():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()   # ← ye line missing thi

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        date TEXT,
        image TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


# -------- HOME PAGE --------
@app.route("/")
def home():
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = cursor.fetchall()
    conn.close()

    return render_template("index.html", posts=posts)

# -------- ADD POST --------
@app.route("/add", methods=["GET","POST"])
def add_post():
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        date = request.form["date"]

        image = request.files["image"]
        image_name = image.filename

        if image_name != "":
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], image_name))

        conn = sqlite3.connect("blog.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts (title,content,date,image) VALUES (?,?,?,?)",
                       (title,content,date,image_name))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("add_post.html")

# -------- DELETE POST --------
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("blog.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
