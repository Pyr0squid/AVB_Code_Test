from flask import render_template
from Backend.api import app, run
from Backend.Database.db import create_db_instance

@app.route("/")
def index():
  return render_template("index.html")

if __name__ == "__main__":
  create_db_instance("Backend/Database/schema.sql", "Backend/Database/database.db")
  run()