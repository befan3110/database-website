from flask import Flask, request, render_template, g
import sqlite3

# Import Flask and other necessary modules
app = Flask(__name__)
DB_DND = "DND.db"
DB_DND2 = "DND2.db"
def get_db_albums():
    if "db" not in g:
        g.db = sqlite3.connect(DB_DND2)
        g.db.row_factory = sqlite3.Row  # optional, for dict-like rows
    return g.db

def get_db_users():
    if "db" not in g:
        g.db = sqlite3.connect(DB_DND)
        g.db.row_factory = sqlite3.Row  # optional, for dict-like rows
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# Define the main route for the application
@app.route("/beatles")
def beatles_page():
    db = get_db_albums()
    cur = db.execute("SELECT title, yyear FROM album")
    data = cur.fetchall()
    members = {"members": [dict(u) for u in data]}
    return render_template("albums.html", title="Welcome", members=members)

@app.route("/")
def front_page():
    user_db = get_db_users()
    cur = user_db.execute("SELECT uid, uname, password FROM user")
    data = cur.fetchall()
    users = {"users": [dict(u) for u in data]}
    return render_template("index.html", title="Welcome", users=users)
    
# Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)