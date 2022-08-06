from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    __tablename__='users'

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    username = db.Column(
        db.String(20),
        nullable=False,
        unique=True
    )
    password = db.Column(db.Text, nullable=False)
    drink = db.relationship('Drink', backref='user')
    @classmethod
    def register(cls, username, password):
        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username,
            password=hashed_utf8
        )
        db.session.add(user)
        return user
    @classmethod
    def authenticate(cls, username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

class Drink(db.Model):
    __tablename__='drinks'

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    drink_name = db.Column(db.Text, nullable=False)
    
    username = db.Column(db.Text, db.ForeignKey('users.username'))


