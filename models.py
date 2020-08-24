"""SQLAlchemy models for capstone1."""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    first_name = db.Column(
        db.Text,
        nullable=True,
        
    )
    last_name = db.Column(
        db.Text,
        nullable=True,
        
    )
    password = db.Column(
        db.Text,
        nullable=False,
    )
    image_url = db.Column(
        db.Text,
        default="/static/img/default-pic.png",
    )
    favorites = db.relationship('UserFavorite')


    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    
    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """
        hashed_pwd = bcrypt.generate_password_hash(password).decode("utf8")

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            
            return user
        else:
            return False
        
    

class Tag(db.Model):
    """Add a tag."""

    __tablename__ = 'tags'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    tag_name = db.Column(
        db.String(140),
        unique=True,
        nullable=False
    )
class UserFavorite(db.Model):
    """Mapping users to liked colleges."""

    __tablename__ = 'user_favorites' 

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    college_id = db.Column(
        db.Integer,
        nullable=False
    )
    college_name = db.Column(
        db.String(140),
        nullable=False
    )
    notes = db.Column(
        db.Text,
        nullable=True
    )
    tags = db.relationship("Tag",secondary="user_college_tags", backref="user_favorites")
    
    def serialize_favorites(self):
        """Serialize SQLAlchemy obj to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "college_id": self.college_id,
            "college_name": self.college_name,
            "notes": self.notes,
        }
    
class UserCollegeTag(db.Model):
    """Mapping user favorited colleges to tags """

    __tablename__ = "user_college_tags"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    user_favorite_id = db.Column(
        db.Integer,
        db.ForeignKey('user_favorites.id', ondelete ='cascade'),
        primary_key=True
    )
    tag_id = db.Column(
        db.Integer,
        db.ForeignKey('tags.id', ondelete ='cascade'),
        primary_key=True
    )

def connect_db(app):
    """Connect this database to provided Flask app.  """

    db.app = app
    db.init_app(app)