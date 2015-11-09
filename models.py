import datetime

from app import db, flask_bcrypt


class User(db.Document):
    email = db.EmailField(unique=True)
    password = db.StringField(default=True)
    active = db.BooleanField(default=True)
    is_superuser = db.BooleanField(default=False)
    is_staff = db.BooleanField(default=False)
    last_login = db.DateTimeField(default=datetime.datetime.now())
    date_joined = db.DateTimeField(default=datetime.datetime.now())
    authenticated = db.BooleanField(default=False)


    def set_password(self, password):
        self.password = flask_bcrypt.generate_password_hash(password)

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password, password)

    def is_anonymous(self):
        return not self.authenticated

    def is_active(self):
        return self.active

    def is_authenticated(self):
        return self.authenticated

    def get_id(self):
        return self.id