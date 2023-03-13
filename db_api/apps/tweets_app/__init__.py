from flask import Blueprint

tweets = Blueprint('tweets', __name__, url_prefix='/tweets')

from . import views