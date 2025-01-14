from .handlers import *


wb_api = fl.Blueprint('wb_api', __name__)


@wb_api.route("/", methods=["GET", "POST"])
def home_route():
    return home()


@wb_api.route("/positive", methods=["GET"])
def get_all_positive_review_route():
    return get_all_positive_review()


@wb_api.route("/positive/<int:page>", methods=["GET"])
def get_positive_review_route(page):
    return get_positive_review(page)


@wb_api.route("/negative", methods=["GET"])
def get_all_negative_review_route():
    return get_all_negative_review()


@wb_api.route("/negative/<int:page>", methods=["GET"])
def get_negative_review_route(page):
    return get_negative_review(page)


@wb_api.route('/search', methods=["GET"])
def search_by_keyword_q_route():
    return search_by_keyword_q()


@wb_api.route('/get', methods=["POST", "GET"])
def get_route():
    return get()


@wb_api.route('/product', methods=["GET"])
def get_mean_product_mark_q_route():
    return get_mean_product_mark_q()


@wb_api.route('/matchSize', methods=["GET"])
def match_size_route():
    return match_size()


@wb_api.route('/color', methods=["GET"])
def search_by_color_q_route():
    return search_by_color_q()


@wb_api.route("/count", methods=["GET"])
def count_reviews_route():
    return count_reviews()
