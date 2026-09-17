from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def conectar_banco():
    conexao = sqlite3.connect("banco.db")
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_banco():
    conexao = conectar_banco()
    conexao.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL
        )
    """)
    conexao.commit()
    conexao.close()


@app.route("/")
def index():
    conexao = conectar_banco()
    produtos = conexao.execute(
        "SELECT * FROM produtos ORDER BY id DESC"
    ).fetchall()
    conexao.close()
    return render_template("index.html", produtos=produtos)


@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        nome = request.form["nome"]
        categoria = request.form["categoria"]
        preco = request.form["preco"]
        estoque = request.form["estoque"]

        conexao = conectar_banco()
        conexao.execute(
            "INSERT INTO produtos (nome, categoria, preco, estoque) VALUES (?, ?, ?, ?)",
            (nome, categoria, preco, estoque)
        )
        conexao.commit()
        conexao.close()
        return redirect("/")
    return render_template("cadastro.html")


@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conexao = conectar_banco()
    produto = conexao.execute(
        "SELECT * FROM produtos WHERE id = ?",
        (id,)
    ).fetchone()

    if request.method == "POST":
        nome = request.form["nome"]
        categoria = request.form["categoria"]
        preco = request.form["preco"]
        estoque = request.form["estoque"]

        conexao.execute(
            "UPDATE produtos SET nome = ?, categoria = ?, preco = ?, estoque = ? WHERE id = ?",
            (nome, categoria, preco, estoque, id)
        )
        conexao.commit()
        conexao.close()
        return redirect("/")

    conexao.close()
    return render_template("editar.html", produto=produto)


@app.route("/excluir/<int:id>")
def excluir(id):
    conexao = conectar_banco()
    conexao.execute("DELETE FROM produtos WHERE id = ?", (id,))
    conexao.commit()
    conexao.close()
    return redirect("/")


if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)
