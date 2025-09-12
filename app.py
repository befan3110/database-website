from flask import Flask, request, render_template, g
import sqlite3

# Import Flask and other necessary modules
app = Flask(__name__)
DB_DND = "DND.db"
DB_DND2 = "DND2.db"

def get_db_classes():
    if "db_classes" not in g:
        g.db_classes = sqlite3.connect(DB_DND2)
        g.db_classes.row_factory = sqlite3.Row  # optional, for dict-like rows
    return g.db_classes

def get_db_spells():
    if "db_spells" not in g:
        g.db_spells = sqlite3.connect(DB_DND)
        g.db_spells.row_factory = sqlite3.Row  # optional, for dict-like rows
    return g.db_spells

@app.teardown_appcontext
def close_db(exception):
    db_classes = g.pop("db_classes", None)
    if db_classes is not None:
        db_classes.close()

    db_spells = g.pop("db_spells", None)
    if db_spells is not None:
        db_spells.close()

# Define the main route for the application
@app.route("/DND_classes")
def classes_page():
    classes_db = get_db_classes()
    cur = classes_db.execute("SELECT class, descriptor FROM classes")
    data = cur.fetchall()
    members = {"members": [dict(u) for u in data]}
    return render_template("classes.html", title="Welcome", members=members)

@app.route("/DND_spells")
def spells_page():
    spells_db = get_db_spells()
    cur = spells_db.execute("SELECT name, level, school FROM spells")
    data = cur.fetchall()
    users = {"users": [dict(u) for u in data]}
    return render_template("spells.html", title="Welcome", users=users)
    
# Start Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)