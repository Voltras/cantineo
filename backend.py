from flask import Flask, request, jsonify, send_from_directory
import sqlite3
import json
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('cantine.db')
    conn.row_factory = sqlite3.Row
    return conn

# Initialisation de la base de données
def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS employes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nom TEXT NOT NULL,
                            prenom TEXT NOT NULL)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS paiement  (
                            id_paiement INTEGER PRIMARY KEY AUTOINCREMENT,
                            date_paiement DATE NOT NULL,
                            montant_paiement FLOAT)
                        ''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS repas (
                            id_repas INTEGER PRIMARY KEY AUTOINCREMENT,
                            employe_id INTEGER NOT NULL,
                            date DATE NOT NULL,
                            id_paiement INTEGER NOT NULL,
                            FOREIGN KEY(employe_id) REFERENCES employes(id),
                            FOREIGN KEY(id_paiement) REFERENCES paiement(id_paiement))''')
        conn.commit()
        cursor.close()

def reset_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS employes")
        cursor.execute("DROP TABLE IF EXISTS repas")
        cursor.close()

reset_db()
init_db()

def get_donnes_test_file():
    with open("donnestest.json", "r") as f:
        return json.load(f)

@app.route('/employes', methods=['GET', 'POST'])
def manage_employes():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO employes (nom, prenom) VALUES (?, ?)", (data['nom'], data['prenom']))
        conn.commit()
        return jsonify({"message": "Employé ajouté !"}), 201
    else:
        employes = cursor.execute("SELECT * FROM employes").fetchall()
        return jsonify([dict(emp) for emp in employes])

@app.route('/repas', methods=['POST'])
def enregistrer_repas():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    for repas in data['repas']:
        cursor.execute("INSERT INTO paiement(montant_paiement, date_paiement) VALUES(?, ?)", (repas['montant'], data['date']))
        id_paiement = cursor.execute("SELECT LAST_INSERT_ROWID();").fetchone()[0]
        print("test")
        print(id_paiement)
        donnestestfile = get_donnes_test_file()
        donnestestfile["id_paiement"] = id_paiement
        with open("donnestest.json", "w") as f:
            json.dump(donnestestfile, f)
        cursor.execute("INSERT INTO repas (employe_id, id_paiement, date) VALUES (?, ?, ?)",
                       (repas['employe_id'], id_paiement, data['date']))
    cursor.close()
    conn.commit()
    return jsonify({"message": "Repas enregistrés !"})

@app.route('/payer', methods=['GET', 'POST'])
def gerer_dettes():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        data = request.json
        cursor.execute("INSERT INTO paiement(montant_paiement, date_paiement) VALUES(?, ?)", (data['montant'], datetime.now()))
        conn.commit()
        return jsonify({"message": "Dette réglée !"})
    else:
        dettes = cursor.execute("SELECT id, prenom, nom, dette FROM employes WHERE dette > 0").fetchall()
        return jsonify([dict(dette) for dette in dettes])

@app.route('/', methods=['GET'])
def serve_frontend():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
