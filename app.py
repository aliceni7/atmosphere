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

# m49 = {}
# reader = csv.reader(open("./data/M49.csv", "r"))
# for row in reader:
# print(row)
# m49[row[0]] = row[1]

# print(m49)

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
	if "username" in session:
		return redirect("/welcome")
	else:
		return render_template("register.html")
@app.route("/welcome")
def welcome():
	if "username" in session:
		return render_template("welcome.html", username = session["username"])
	else:
		return redirect("/login")



@app.route("/auth")
def auth():
	command = "SELECT * FROM loginfo WHERE username like '{}'".format(
		request.args["username"])
	pair = runsqlcommand(command)
	print("#######")
	print(pair)
	if len(pair) == 0:
		return "username not found"
	if pair[0][0] == request.args["username"]:
		if pair[0][1] == request.args["password"]:
			session["username"] = request.args["username"]
			return redirect("/login")
		return "wrong password"
	return "wrong username"


@app.route("/logout")
def logout():
	session.pop("username")
	return redirect("/login")



@app.route("/lookup")
def lookup():
	r = urllib.request.urlopen(
		"https://apps.bea.gov/api/data/?&UserID=1B07B684-579E-4E91-8517-DA093A82DA43&method=GetData&datasetname=Regional&TableName=SAINC1&GeoFIPS=STATE&LineCode=3&Year=2018&ResultFormat=JSON"  # Some API link goes here
	)
	data = json.loads(r.read())
	print(data)
	# caches data to the data/ directory
	with open('./data/income.json', 'w') as outfile:
		json.dump(data, outfile, indent=4)
	# print(data['results'][0]['name'])
	return render_template("lookup.html", data=data)


if __name__ == "__main__":
	app.debug = True
	app.run()
