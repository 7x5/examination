from flask import *

import sqlite3

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/registration")
def registration():
    return render_template("registration.html")

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
                cur.execute("INSERT into RUSS (fornavn, etternavn, epost, telefon) values (?,?,?,?)",(fnavn,enavn,epost,telenr))  
                con.commit()  
                msg = "student successfully Added"  
        except:  
            con.rollback()  
            msg = "We can not add the employee to the list"  
        finally:  
            con.close()  
            return render_template("success.html",msg = msg)  
            

app.run(host="0.0.0.0", port=5001)