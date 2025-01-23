from flask import Flask
from backend.models import User
from backend.database import db
from werkzeug.security import generate_password_hash

app = Flask(__name__)

@app.cli.command("create-superuser")
def create_superuser():
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    superuser = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        is_superuser=True
    )
    db.session.add(superuser)
    db.session.commit()
    print("Superuser created successfully!")
