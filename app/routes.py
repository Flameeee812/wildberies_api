from .handlers import *


blueprint = fl.Blueprint('wb_api', __name__)


@blueprint.route("/", methods=["GET", "POST"])
def home_route():
    return home()


@blueprint.route("/positive", methods=["GET"])
def get_all_positive_review_route():
    return get_all_positive_review()


@blueprint.route("/positive/<int:page>", methods=["GET"])
def get_positive_review_route(page):
    return get_positive_review(page)


@blueprint.route("/negative", methods=["GET"])
def get_all_negative_review_route():
    return get_all_negative_review()


@blueprint.route("/negative/<int:page>", methods=["GET"])
def get_negative_review_route(page):
    return get_negative_review(page)


@blueprint.route('/search', methods=["GET"])
def search_by_keyword_q_route():
    return search_by_keyword_q()


@blueprint.route('/get', methods=["POST", "GET"])
def get_route():
    return get()


@blueprint.route('/product', methods=["GET"])
def get_mean_product_mark_q_route():
    return get_mean_product_mark_q()


@blueprint.route('/matchSize', methods=["GET"])
def match_size_route():
    return match_size()


@blueprint.route('/color', methods=["GET"])
def search_by_color_q_route():
    return search_by_color_q()


@blueprint.route("/count", methods=["GET"])
def count_reviews_route():
    return count_reviews()
