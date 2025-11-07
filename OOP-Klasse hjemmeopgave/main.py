from database import Database

db = Database()

# Tilføj ny klasse
db.insert("bloodhunter", "strength", "fights using cursed blood magic")

# Søg efter klasser med "wisdom"
print(db.search("wisdom"))

# Hent en klasse fra id
print(db.load(3))  # for eksempel bard

# Hent alle
print(db.load_all())
