from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
import mysql.connector
import os

app = Flask(__name__)
load_dotenv()

MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

db = mysql.connector.connect(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, database=MYSQL_DB)

@app.route("/")
def index():
  cursor = db.cursor(dictionary=True)
  cursor.execute("SELECT * FROM users")
  result = cursor.fetchall()
  return render_template("home.html", users=result)

@app.route("/insert", methods=["GET", "POST"])
def insert():
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    db.commit()
    return redirect("/")
    
  return render_template("insert.html")

if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)