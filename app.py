import json
import pandas as pd
import flask as fl
from flask_caching import Cache


api_db = pd.read_csv("prepared_data.csv",
                     sep=",")

api = fl.Flask(__name__)

api.config['CACHE_TYPE'] = 'simple'
cache = Cache(api)


class Products:
    def __init__(self, new_index="Unnamed: 0"):
        self._index = new_index
        self.error = f"The column '{self._index}' cannot be used as an index for this function."
        self.new_index_data = api_db.set_index(new_index)

    def get_pos_rev(self):
        return self.new_index_data["mark"][self.new_index_data["mark"] > 3]

    def get_neg_rev(self):
        return self.new_index_data["mark"][self.new_index_data["mark"] <= 3]

    def search_by_word(self, word):
        return self.new_index_data["text"][self.new_index_data["text"].str.contains(word, na=False)]

    def get_buyer_rev(self, reviewer_name, products):
        filtered_data = self.new_index_data.loc[products]
        return filtered_data[filtered_data["reviewerName"] == reviewer_name]["text"]

    def search_by_color(self, color):
        return self.new_index_data["color"][self.new_index_data["color"] == color]

    def match_size(self):
        return self.new_index_data["matchingSize"][
            self.new_index_data["has_sizes"].values & (self.new_index_data["matchingSize"] == "ok")
        ]

    @staticmethod
    def get_product(word):
        return round(api_db.groupby(
            api_db[api_db["name"].str.contains(word, na=False)]["name"]
        )["mark"].mean(), 1)

    def count_rev(self):
        return self.new_index_data.groupby("name")["text"].count().to_dict()


@api.route("/", methods=["GET", "POST"])
def home_page() -> object:
    """Function that displays the home page"""

    if fl.request.method == "POST":
        pos_page = fl.request.form.get("pos_page")
        neg_page = fl.request.form.get("neg_page")
        search_by_word = fl.request.form.get("search_by_word")
        average_rating = fl.request.form.get("average_rating")
        color = fl.request.form.get("color")

        if pos_page:
            return fl.redirect(fl.url_for("get_positive_review", page=pos_page))
        elif neg_page:
            return fl.redirect(fl.url_for("get_negative_review", page=neg_page))
        elif search_by_word:
            return fl.redirect(fl.url_for("search_by_keyword_q", q=search_by_word))
        elif average_rating:
            return fl.redirect(fl.url_for("get_mean_product_mark_q", name=average_rating))
        elif color:
            return fl.redirect(fl.url_for("search_by_color_q", color=color))
        else:
            return fl.render_template("index.html")
    else:
        return fl.render_template("index.html")


@cache.cached(timeout=60)
@api.route("/positive")
def get_all_positive_review() -> object:
    """Function that displays all positive
    reviews for the "/positive route" """

    data = Products("text")
    try:
        return fl.jsonify({
            "pos_review": data.get_pos_rev().to_dict()
        })
    except KeyError:
        return data.error


@api.route("/positive/<int:page>")
def get_positive_review(page) -> object:
    """Function that displays positive
    reviews for the "/positive/page" route

    Parameters:
    1. page - the page number with reviews"""

    data = Products("text")
    try:
        return fl.jsonify({
            "pos_review": data.get_pos_rev()[(100 * (page - 1)):(100 * page)].to_dict()
        })
    except KeyError:
        return data.error


@cache.cached(timeout=60)
@api.route("/negative")
def get_all_negative_review() -> object:
    """Function that displays all positive
     reviews for the "/negative" route"""

    data = Products("text")
    try:
        return fl.jsonify({
            "neg_review": data.get_neg_rev().to_dict()
        })
    except KeyError:
        return data.error


@api.route("/negative/<int:page>")
def get_negative_review(page) -> object:
    """Function that displays negative reviews for the "/positive/page" route

    Parameters:
    1. page - the page number with reviews"""

    data = Products("text")
    try:
        return fl.jsonify({
            "neg_review": data.get_neg_rev()[(100 * (page - 1)):(100 * page)].to_dict()
        })
    except KeyError:
        return data.error


@api.route('/search')
def search_by_keyword_q() -> object:
    """Function that search all products
    by word for the "/search?q=" route"""

    data = Products("name")
    try:
        return fl.jsonify({
            "results": data.search_by_word(fl.request.args.get("q")).to_dict()
        })
    except KeyError:
        return data.error


@api.route('/get', methods=["POST", "GET"])
def get():
    """Function that displays an HTML page with
    buyer reviews for a POST request"""

    if fl.request.method == "POST":
        json_object = fl.request.form["JSON"]
        json_obj = json.loads(json_object)
        # json_obj = fl.request.json       |postman|
        data = Products("name")

        try:
            return data.get_buyer_rev(
                reviewer_name=json_obj["reviewerName"], products=json_obj["name"]
            ).to_dict()
        except KeyError:
            return data.error

    else:
        return fl.render_template("get.html")


@cache.cached(timeout=60)
@api.route('/product')
def get_mean_product_mark_q():
    """Function that displays the average rating
    of a product by name for "/product" route """

    return fl.jsonify({
        "means": [Products.get_product(fl.request.args.get("name")).to_dict()]
        })


@api.route('/matchSize')
def match_size() -> object:
    """Function that displays products that are in stock
    and fit the size for "/matchSize" route"""

    data = Products("name")
    try:
        return fl.jsonify({
           "ok_size": data.match_size().to_dict()
        })
    except KeyError:
        return data.error


@api.route('/color')
def search_by_color_q() -> object:
    """Function that search all products
    by color for the "/search?color=" route"""

    data = Products("name")
    try:
        return fl.jsonify({
            "right_color": data.search_by_color(fl.request.args.get("color")).to_dict()
        })
    except KeyError:
        return data.error


@api.route("/count")
def count_reviews() -> object:
    """Function that count all reviews
    for a product for the "/search?q=" route"""

    data = Products()
    try:
        return fl.jsonify({
           "count_review": data.count_rev()
        })
    except KeyError:
        return data.error


if __name__ == "__main__":
    api.run(debug=True, port=5001)
