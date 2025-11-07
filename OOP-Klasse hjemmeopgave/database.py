import sqlite3

DB_DND = "dndclass.db"  #class-databasen(fordi den anden er lidt for kompliceret)

class Database:
    def _connect(self):
        #Opret og returner en databaseforbindelse
        conn = sqlite3.connect(DB_DND)
        conn.row_factory = sqlite3.Row
        return conn

    def _execute(self, query, params=()):
        #lav en INSERT, UPDATE eller DELETE
        conn = self._connect()
        try:
            conn.execute(query, params)
            conn.commit()
        finally:
            conn.close()

    def _run_query(self, query, params=()):
        #Kører SELECT
        conn = self._connect()
        try:
            cur = conn.execute(query, params)
            rows = cur.fetchall()
        finally:
            conn.close()
        return [dict(row) for row in rows]


    def search(self, term):
        #Søger efter DND Classes ud fra navn eller ability
        query = """
            SELECT * FROM dnd5_classes
            WHERE class_name LIKE ? OR class_ability LIKE ?
        """
        params = (f"%{term}%", f"%{term}%")
        return self._run_query(query, params)

    def load(self, class_id):
        #Hent en klasse ud fra id
        query = "SELECT * FROM dnd5_classes WHERE class_id = ?"
        rows = self._run_query(query, (class_id,))
        return rows[0] if rows else None

    def load_all(self):
        #Hent alle klasser
        query = "SELECT * FROM dnd5_classes"
        return self._run_query(query)

    def insert(self, class_name, class_ability, class_description):
        #Tilføj en ny class
        query = """
            INSERT INTO dnd5_classes (class_name, class_ability, class_description)
            VALUES (?, ?, ?)
        """
        self._execute(query, (class_name, class_ability, class_description))
