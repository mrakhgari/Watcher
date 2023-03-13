from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 


from directory.configs import Production


app = Flask(__name__)
app.config.from_object(Production)


db = SQLAlchemy(app, session_options={"autoflush": False})
migrate = Migrate(app, db)



from directory.apps.users_app import users
from directory.apps.tweets_app import tweets

app.register_blueprint(users)
app.register_blueprint(tweets)
