from flask import Flask, render_template, abort
import json

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)
