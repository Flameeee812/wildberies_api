import flask as fl
from .routes import wb_api


api_app = fl.Flask(__name__, template_folder="../templates")
api_app.register_blueprint(wb_api, url_prefix="/wb_api")
