import flask as fl

from .routes import blueprint


app = fl.Flask(__name__, template_folder="../templates")
app.register_blueprint(blueprint, url_prefix="/wb_api")
