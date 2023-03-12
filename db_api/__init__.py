from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 


from db_api.configs import Production


app = Flask(__name__)
app.config.from_object(Production)


db = SQLAlchemy(app, session_options={"autoflush": False})
migrate = Migrate(app, db)


@app.route('/')
def hello_world():
    return {'message' : "Welcome To Ziriland!"}



from db_api.apps.users_app import users

# from directory.apps.users_app import users
# from directory.apps.subscriptions_app import subscriptions
# from directory.apps.servers_app import servers

app.register_blueprint(users)
# app.register_blueprint(subscriptions)
# app.register_blueprint(servers)
