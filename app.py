from flask import Flask, request, render_template, g
import sqlite3

# Importer flask
app = Flask(__name__)
DB_DND = "dndclass.db"
DB_DND2 = "dndspells.db"


def get_db_classes():
# henter vores database    
    if "db_classes" not in g:
        g.db_classes = sqlite3.connect(DB_DND)
        g.db_classes.row_factory = sqlite3.Row
    return g.db_classes

def get_db_spells():
# henter vores database    
    if "db_spells" not in g:
        g.db_spells = sqlite3.connect(DB_DND2)
        g.db_spells.row_factory = sqlite3.Row
    return g.db_spells

@app.teardown_appcontext
# lukker vores database
def close_db(exception):
    db_classes = g.pop("db_classes", None)
    if db_classes is not None:
        db_classes.close()

@app.teardown_appcontext
# lukker vores database
def close_db(exception):
    db_spells = g.pop("db_spells", None)
    if db_spells is not None:
        db_spells.close()


@app.route("/")
def main_page():

    return render_template("dnd.html", title="Arcane Compendium")

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
            # henter dataen for vores søgning
            data = cur.fetchall()
            cur.close()

            members = {"members": [dict(u) for u in data], "show_description": show_description}

    return render_template("classes.html", title="class-site", members=members)
    # returnerer vores værdier til html siden


# vores funktion til at søge i databasen
@app.route("/DND_spells", methods=["GET", "POST"])
def spells_page():
    db_spells = get_db_spells()
    
    query = None
    params = ()
    members = {"members": []}

    if request.method == "POST":
        search_term = request.form.get("search_term", "").strip()
        if search_term:
            # søger
            query = """
                SELECT spell_id, spell_name, spell_level, casting_time, spell_range, components, duration, description, higher_levels
                FROM dnd5_spells
                WHERE spell_name LIKE ? OR spell_level LIKE ?
            """
            params = (f"%{search_term}%", f"%{search_term}%")

            cur = db_spells.execute(query, params)
            # henter dataen for vores søgning
            data = cur.fetchall()
            cur.close()

            members = {"members": [dict(u) for u in data]}

    return render_template("spells.html", title="spell-site", members=members)
    # returnerer vores værdier til html siden

@app.route("/documentation")
def doc_page():

    return render_template("doc.html", title="Documentation")    

# Starter Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)