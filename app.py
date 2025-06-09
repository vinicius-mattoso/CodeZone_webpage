from flask import Flask, render_template, request, redirect, flash, abort
import csv
from datetime import datetime
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/trilhas")
def trilhas():
    with open("data/trilhas.json", "r", encoding="utf-8") as f:
        trilhas = json.load(f)
    return render_template("trilhas.html", trilhas=trilhas)

@app.route("/trilha/<slug>")
def trilha_detalhe(slug):
    with open("data/conteudos.json", "r", encoding="utf-8") as f:
        conteudos = [c for c in json.load(f) if c["trilha"] == slug]

    with open("data/trilhas.json", "r", encoding="utf-8") as f:
        trilhas = json.load(f)
        trilha = next((t for t in trilhas if t["slug"] == slug), None)

    if not trilha:
        abort(404)

    return render_template("trilha_detalhe.html", trilha=trilha, conteudos=conteudos)

@app.route("/blog")
def blog():
    return render_template("blog.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        assunto = request.form['assunto']
        mensagem = request.form['mensagem']
        data_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Caminho do CSV
        caminho_csv = "contatos.csv"
        arquivo_existe = os.path.exists(caminho_csv)

        try:
            with open(caminho_csv, "a", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)

                # Escreve cabeçalho se for novo
                if not arquivo_existe:
                    writer.writerow(["Nome", "Email", "Assunto", "Mensagem", "Data"])

                writer.writerow([nome, email, assunto, mensagem, data_envio])

            flash("Mensagem enviada com sucesso!", "success")
        except Exception as e:
            print("Erro ao salvar no CSV:", e)
            flash("Erro ao enviar sua mensagem. Tente novamente mais tarde.", "danger")

        return redirect("/contato")

    return render_template("contato.html")

@app.route("/blog/python-mercado")
def blog_python():
    return render_template("blog/python-mercado.html")

@app.route("/blog/ia-resultados")
def blog_ia():
    return render_template("blog/ia-resultados.html")

if __name__ == "__main__":
    app.run(debug=True)
