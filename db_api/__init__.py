from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 


from db_api.configs import Production


app = Flask(__name__)
app.config.from_object(Production)


db = SQLAlchemy(app, session_options={"autoflush": False})
migrate = Migrate(app, db)



from db_api.apps.users_app import users
from db_api.apps.tweets_app import tweets

app.register_blueprint(users)
app.register_blueprint(tweets)
