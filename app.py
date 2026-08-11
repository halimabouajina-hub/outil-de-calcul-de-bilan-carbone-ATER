from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def accueil():
    return render_template("accueil.html")

@app.route("/individu")
def individu():
    return render_template("individu.html")

@app.route("/scope1")
def scope1():
    return render_template("scope1.html")

if __name__ == "__main__":
    app.run(debug=True) 
    