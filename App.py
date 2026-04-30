from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# 🔧 création base de données
def init_db():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS etudiants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT,
            n1 REAL,
            n2 REAL,
            n3 REAL,
            moyenne REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/add', methods=['POST'])
def add():
    nom = request.form['nom']
    n1 = float(request.form['note1'])
    n2 = float(request.form['note2'])
    n3 = float(request.form['note3'])

    moyenne = (n1 + n2 + n3) / 3

    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO etudiants (nom, n1, n2, n3, moyenne)
        VALUES (?, ?, ?, ?, ?)
    """, (nom, n1, n2, n3, moyenne))
    conn.commit()
    conn.close()

    return redirect('/result')

@app.route('/result')
def result():
    conn = sqlite3.connect("notes.db")
    c = conn.cursor()
    c.execute("SELECT nom, moyenne FROM etudiants ORDER BY moyenne DESC")
    data = c.fetchall()
    conn.close()

    etudiants = [{"nom": d[0], "moyenne": d[1]} for d in data]

    noms = [e["nom"] for e in etudiants]
    moyennes = [e["moyenne"] for e in etudiants]

    moyenne_classe = sum(moyennes) / len(moyennes) if moyennes else 0

    return render_template(
        "result.html",
        etudiants=etudiants,
        noms=noms,
        moyennes=moyennes,
        moyenne_classe=moyenne_classe,
        notes=moyennes
    )

if __name__ == "__main__":
    import os

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    app.run(debug=True)