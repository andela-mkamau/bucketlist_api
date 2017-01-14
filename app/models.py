import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    The User creates and manages bucketlists.
    At the database level, users are stored within a table : `users`
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    bucketlists = db.relationship('Bucketlist', backref='created_by',
                                  lazy='dynamic', cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def to_json(self):
        return {
            'username': self.username
        }

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "User: {}".format(self.username)


class Bucketlist(db.Model):
    """
    A Bucketlist represents a collection of Items managed by the User.
    Each Bucketlist must be owned by a User; and can have multiple Items within
    it.
    At the database level, Bucketlists are stored in the table `bucketlists`.
    """
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    description = db.Column(db.String(1000), default="")
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
    date_modified = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship('Item', backref='bucketlist', lazy='dynamic',
                            cascade='all, delete-orphan')

    def __repr__(self):
        return "Bucketlist: {}".format(self.name)


class Item(db.Model):
    """
    An Item represents an entry on the Bucketlist.
    At the database level, Items are stored in the table `items`
    """
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False, index=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
    date_modified = db.Column(db.DateTime)
    done = db.Column(db.Boolean, default=False)
    priority = db.Column(db.String(100))
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def __repr__(self):
        return "Item: {}".format(self.name)
