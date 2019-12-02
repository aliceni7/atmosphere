# Joseph Yusufov, Mudadour Rahman, Alice Ni, David Wang
# SoftDev1 pd2
# Atmosphere
# 2019-11-xx

from flask import Flask, render_template, request, session
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import flash
from flask import url_for
import urllib
import json
import random
import csv
import sqlite3
import os
from util import cache

cache.cache()

states = {}
reader = csv.reader(open("./data/states.csv", "r"))
# for row in reader:
#     print(row)
#     states[row[0]] = row[1]

IDtoAlpha = {}
reader = csv.reader(open("./data/id-to-alpha.csv", "r"))
# for row in reader:
#     print(row)
#     IDtoAlpha[row[0]] = row[1]


app = Flask(__name__)  # create instance of class Flask
app.secret_key = os.urandom(24)


def runsqlcommand(command):
    DB_FILE = "data.db"
    db = sqlite3.connect(DB_FILE)  # open if file exists, otherwise create
    c = db.cursor()  # facilitate db ops
    c.execute(command)
    if "select" in command.lower():
        return c.fetchall()
    db.commit()  # save changes
    db.close()  # close database


@app.route("/")  # assign following fxn to run when root route requested
def index():
    return render_template('index.html')


@app.route("/login")
def login():
    if "username" in session:
        return redirect("/welcome")
    else:
        return render_template("login.html")


@app.route("/register")
def register():
    if len(request.args) > 0:
        username = request.args["username"]
        password = request.args["password"]
        confirm = request.args["confirm"]
        existence_command = "SELECT * FROM loginfo WHERE username LIKE '{}'".format(
            username)
        names = runsqlcommand(existence_command)
        if len(names) != 0:
            flash("Username already taken")
            return redirect("/register")
        if password != confirm:
            flash("Password and confirmation don't match")
            return redirect("/register")
        else:
            insert_username = "INSERT INTO loginfo VALUES ('{}', '{}')".format(
                username, password)
            runsqlcommand(insert_username)
            flash("Successful registration")
            return redirect("/login")
    if "username" in session:
        return redirect("/welcome")
    else:
        return render_template("register.html")


@app.route("/welcome")
def welcome():
    if "username" in session:
        r = urllib.request.urlopen("https://api.census.gov/data/2018/pep/population?get=POP&for=us:*&key=07626e3b3578edd0e55ba15cb38770a85aedd31d")
        data = [json.loads(r.read())[1][0]]
        r = urllib.request.urlopen("https://api.census.gov/data/timeseries/poverty/saipe?get=NAME,SAEPOVALL_PT&for=us:*&time=2016")
        data.append(json.loads(r.read())[1][1])
        r = urllib.request.urlopen("https://api.eia.gov/series/?api_key=a646920f26214e3dbdad25a3908f9c5f&series_id=EMISS.CO2-TOTV-IC-TO-US.A")
        data.append(json.loads(r.read())["series"][0]["data"][0][1])
        return render_template("welcome.html", population = data[0], poverty = data[1], emissions = data[2], username=session['username'])
    else:
        return redirect("/login")


@app.route("/auth")
def auth():
    command = "SELECT * FROM loginfo WHERE username LIKE '{}'".format(
        request.args["username"])
    pair = runsqlcommand(command)
    print("#######")
    print(pair)
    if len(pair) == 0:
        flash("Username not found")
        return redirect("/login")
    if pair[0][0] == request.args["username"]:
        if pair[0][1] == request.args["password"]:
            session["username"] = request.args["username"]
            flash("Successfully logged in as: {}".format(session['username']))
            return redirect("/welcome")
        flash("Wrong password")
        return redirect("/login")
    flash("Wrong username")
    return redirect("/login")


@app.route("/logout")
def logout():
    session.pop("username")
    flash("Logged out successfully")
    return redirect("/login")


@app.route("/lookup")
def lookup():
    if 'username' in session:
        if request.args:
            print("\n{}".format(request.args.get('state')))
            alpha = IDtoAlpha[request.args.get('state')]
            print("##########\n{}".format(alpha))
            r = urllib.request.urlopen(
                "https://apps.bea.gov/api/data/?&UserID=1B07B684-579E-4E91-8517-DA093A82DA43&method=GetData&datasetname=Regional&TableName=SAINC1&GeoFIPS=STATE&LineCode=3&Year=2017&ResultFormat=JSON"  # Some API link goes here
            )
            income = json.loads(r.read())

            g = urllib.request.urlopen(
                "https://apps.bea.gov/api/data/?&UserID=1B07B684-579E-4E91-8517-DA093A82DA43&method=GetData&datasetname=Regional&TableName=SAGDP2N&GeoFIPS=STATE&LineCode=3&Year=2017&Frequency=A&ResultFormat=JSON"  # Some API link goes here
            )
            gdp = json.loads(g.read())

            p = urllib.request.urlopen(
                "https://api.eia.gov/series/?api_key=a646920f26214e3dbdad25a3908f9c5f&series_id=EMISS.CO2-TOTV-TT-TO-{}.A".format(
                    alpha)
            )
            co2 = json.loads(p.read())

            f = "http://flags.ox3.in/svg/us/{}.svg".format(alpha.lower())

            print(f)
            # print(data['BEAAPI']['Results']['Data'][1]['DataValue'])
            # print("This should be state ID: {}".format(request.args.get('state')))
            # for member in data:
            # print(member + "\n")
            # CACHING MUST BE DONE WITH Flask-Caching

            # session['IncomeCache'] = data
            # caches data to the data/ directory
            # with open('./data/income.json', 'w') as outfile:
            #     json.dump(data, session['IncomeCache'], indent=4)
            # print(data['results'][0]['name'])
            return render_template("lookup.html", income=income['BEAAPI']['Results']['Data'][int(request.args.get('state'))], gdp=gdp['BEAAPI']['Results']['Data'][(int(request.args.get('state')))], co2=co2, username=session['username'], states=states, flag=f, selected=request.args.get('state'))
        return render_template("lookup.html", username=session['username'], states=states)
    flash("Log in to use Atmo.")
    return redirect("/login")


@app.route("/analysis")
def analysis():
    if 'username' in session:
        if request.args:
            params = [request.args.get('xVar'), request.args.get('yVar')]
            with open("./data/JSON/cache.json", "r") as cachefile:
                cache = json.load(cachefile)
            data = {}
            
            data['x'] = cache[params[0]]
            for member in data['x']['data']:
                data['x']['data'][member] = str(data['x']['data'][member]).replace(',', '')
                                
            data['y'] = cache[params[1]]
            for member in data['y']['data']:
                data['y']['data'][member] = str(data['y']['data'][member]).replace(',', '')
                
            return render_template("analysis.html", username=session['username'], data=data)
        return render_template("analysis.html", username=session['username'])
    flash("Log in to use Atmo.")
    return redirect("/login")



if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
