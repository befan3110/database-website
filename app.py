from flask import Flask, request, render_template, g
import sqlite3

# Importer flask
app = Flask(__name__)
DB_DND = "dndclass.db"


def get_db_classes():
# henter vores database    
    if "db_classes" not in g:
        g.db_classes = sqlite3.connect(DB_DND)
        g.db_classes.row_factory = sqlite3.Row
    return g.db_classes


@app.teardown_appcontext
def close_db(exception):
    db_classes = g.pop("db_classes", None)
    if db_classes is not None:
        db_classes.close()


# vores funktion til at søge i databasen
@app.route("/DND_classes", methods=["GET", "POST"])
def classes_page():
    db_classes = get_db_classes()
    
    query = None
    params = ()
    show_description = False
    members = {"members": [], "show_description": show_description}

    if request.method == "POST":
        # skaffer søgemetoden
        search_term = request.form.get("search_term", "").strip()
        if search_term:
        # søger    
            query = "SELECT class_id, class_name, class_ability, class_description FROM dnd5_classes"
            query += " WHERE class_name LIKE ? OR class_ability LIKE ?"
            params = (f"%{search_term}%", f"%{search_term}%")
            show_description = True

            cur = db_classes.execute(query, params)
            data = cur.fetchall()
            cur.close()

            members = {"members": [dict(u) for u in data], "show_description": show_description}

    return render_template("classes.html", title="Welcome", members=members)
    # returnerer vores værdier til html siden

# Starter Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)