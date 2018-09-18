from flask import Flask
from flask_sqlalchemy import SQLAlchemy # Python ORM

app = Flask(__name__)
app.config["DEBUG"] = True  # set to True for Flask report on web server activity
app.config["SQLALCHEMY_ECHO"] = False   # set True for MySQL report on database activity

# put in your database credentials here
username = "root"
password = ""
host = "localhost"
port = "3306"
database = "user_games"

connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app) # uses the SQLAlchemy Database URI (connection string) to connect to the db
db_session = db.session # used for interaction with the database

# define the owned_games associative table
"""
this table serves purely to manage the Many-to-Many relationship between User and Game
you do not create a Model for it
"""

owned_games = db.Table(
  "owned_games",
  db.Column(
    "user_id",
    db.ForeignKey("users.id"), # the Column the FK refers to
  ),
  db.Column(
    "game_id",
    db.ForeignKey("games.id"),
  ),
)

# define the User Model
"""
a Model is an object-oriented representation of a SQL Table
inherits behavior from the SQLAlchemy (ORM) Model Class 
uses static properties to define Columns

an Object Instance of the Model represents a Row in the corresponding Table
"""
class User(db.Model):
  __tablename__ = "users"

  # Columns
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True)

  # Relationships
  """
  establishes the User relationship to Games 

  accessing a User instance's owned Games by the 'games' property
  user.games --> list of Game objects
  """
  games = db.relationship(
    "Game", # the Model / Table that the relationship is with
    secondary=owned_games, # the secondary / associative Table for the m2m relationship
  )

class GameStudio(db.Model):
  __tablename__ = "game_studios"

  # Columns
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(30), unique=True)

  # Relationships
  """
  establishes the Game Studio relationship to Games 

  by using the 'backref' argument we do not need to write the
  mirror relationship on the Game Model
    it automatically adds a 'studio' property to the Game

  game_studio.games -> list of Game objects
  game.studio -> Game Studio the Game belongs to
  """
  games = db.relationship(
    "Game", # the Model / Table that the relationship is with
    backref="studio",
  )

class Game(db.Model):
  __tablename__ = "games"

  # Columns
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(30), unique=True)
  game_studio_id = db.Column(db.ForeignKey("game_studios.id"), primary_key=True)

  # Relationships
  """
  establishes the Game relationship to Users 

  accessing a Game instance's owner Users by the 'owners' property
  game.owners --> list of User objects
  """
  owners = db.relationship(
    "User", # the Model / Table that the relationship is with
    secondary=owned_games, # the secondary / associative Table for the m2m relationship
   )


def main():
  from sqlalchemy import create_engine, inspect
  from sqlalchemy.exc import OperationalError
  
  try:
    ENGINE = create_engine(connection_string)
    INSPECTOR = inspect(ENGINE)  # used for checking if tables exist on startup

    # check if tables exist - create if they do not
    tables = INSPECTOR.get_table_names()
    if not tables:
        db.create_all()
    
    app.run()

  except OperationalError as error:
    print("Error connecting to the DB, print 'errors' for more detail")


if __name__ == "__main__":
    print(Game.query.all()[0].studio.title)
    main()