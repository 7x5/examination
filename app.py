from flask import *

import sqlite3

import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/register", methods=['POST'])
def register():
    brukernavn = request.form['brukernavn']
    passord = request.form['passord']

    hashed_passord = hashlib.sha256(passord.encode()).hexdigest()

    con = sqlite3.connect('database.db')
    c = con.cursor()
    c.execute("INSERT INTO admin (brukernavn, passord) VALUES (?, ?)", (brukernavn, hashed_passord))
    con.commit()
    con.close()

    return render_template("adminsuccess.html", brukernavn = brukernavn)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        brukernavn = request.form['brukernavn']
        passord = request.form['passord']

        con = sqlite3.connect('database.db')
        c = con.cursor()
        c.execute("SELECT * FROM admin WHERE brukernavn=?", (brukernavn,))
        admin = c.fetchone()
        con.close()

        if admin:
            lagret_passord = admin[2]
            hashed_passord = hashlib.sha256(passord.encode()).hexdigest()
            if lagret_passord == hashed_passord:
                session['logged_in'] = True
                return redirect(url_for('admin_dashboard')) 
            
        return 'Invaild password or username'
    
    return render_template('login.html')

@app.route('/login/dashboard')
def admin_dashboard():
    if 'logged_in' in session and session['logged_in']:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))

@app.route("/savedetails",methods = ["POST","GET"])  
def saveDetails():  
    msg = "msg"
    if request.method == "POST":  
        try:  
            fnavn = request.form["fnavn"] 
            enavn = request.form["enavn"]
            telenr = request.form["telefon"]
            epost = request.form["epost"]
            with sqlite3.connect("database.db") as con:  
                cur = con.cursor()  
                cur.execute("INSERT into RUSS (fornavn, etternavn, epost, telefon, betalt) values (?,?,?,?,?)",(fnavn,enavn,epost,telenr,0))  
                con.commit()  
                msg = "Registert, vennligst betal"  
        except:  
            con.rollback()  
            msg = "Noe gikk galt, prøv igjen om litt"  
        finally:  
            con.close()  
            return render_template("success.html",msg = msg)  
            

app.run(host="0.0.0.0", port=5001)