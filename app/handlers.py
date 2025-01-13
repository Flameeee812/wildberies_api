import flask as fl
import json
import pandas_db


def home():
    if fl.request.method == "POST":
        pos_page = fl.request.form.get("pos_page")
        neg_page = fl.request.form.get("neg_page")
        search_by_word = fl.request.form.get("search_by_word")
        average_rating = fl.request.form.get("average_rating")
        color = fl.request.form.get("color")

        if pos_page:
            return fl.redirect(fl.url_for("wb_api.get_positive_review_route", page=pos_page))
        elif neg_page:
            return fl.redirect(fl.url_for("wb_api.get_negative_review_route", page=neg_page))
        elif search_by_word:
            return fl.redirect(fl.url_for("wb_api.search_by_keyword_q_route", q=search_by_word))
        elif average_rating:
            return fl.redirect(fl.url_for("wb_api.get_mean_product_mark_q_route", name=average_rating))
        elif color:
            return fl.redirect(fl.url_for("wb_api.search_by_color_q_route", color=color))
        else:
            return fl.render_template("index.html")
    else:
        return fl.render_template("index.html")


def get_all_positive_review():
    """Function that displays all positive
    reviews for the "/positive route" """

    data = pandas_db.Products("text")
    try:
        return fl.jsonify({
            "pos_review": data.get_pos_rev().to_dict()
        })
    except KeyError:
        return data.error


def get_positive_review(page):
    """Function that displays positive
    reviews for the "/positive/page" route

    Parameters:
    1. page - the page number with reviews"""

    data = pandas_db.Products("text")
    try:
        return fl.jsonify({
            "pos_review": data.get_pos_rev()[(100 * (page - 1)):(100 * page)].to_dict()
        })
    except KeyError:
        return data.error


def get_all_negative_review():
    """Function that displays all positive
     reviews for the "/negative" route"""

    data = pandas_db.Products("text")
    try:
        return fl.jsonify({
            "neg_review": data.get_neg_rev().to_dict()
        })
    except KeyError:
        return data.error


def get_negative_review(page):
    """Function that displays negative reviews for the "/positive/page" route

    Parameters:
    1. page - the page number with reviews"""

    data = pandas_db.Products("text")
    try:
        return fl.jsonify({
            "neg_review": data.get_neg_rev()[(100 * (page - 1)):(100 * page)].to_dict()
        })
    except KeyError:
        return data.error


def search_by_keyword_q():
    """Function that search all products
    by word for the "/search?q=" route"""

    data = pandas_db.Products("name")
    try:
        return fl.jsonify({
            "results": data.search_by_word(fl.request.args.get("q")).to_dict()
        })
    except KeyError:
        return data.error


def get():
    """Function that displays an HTML page with
    buyer reviews for a POST request"""

    if fl.request.method == "POST":
        json_object = fl.request.form["JSON"]
        json_obj = json.loads(json_object)
        # json_obj = fl.request.json       |postman|
        data = pandas_db.Products("name")

        try:
            return data.get_buyer_rev(
                reviewer_name=json_obj["reviewerName"], products=json_obj["name"]
            ).to_dict()
        except KeyError:
            return data.error

    else:
        return fl.render_template("get.html")


def get_mean_product_mark_q():
    """Function that displays the average rating
    of a product by name for "/product" route """

    return fl.jsonify({
        "means": [pandas_db.Products.get_product(fl.request.args.get("name")).to_dict()]
        })


def match_size():
    """Function that displays products that are in stock
    and fit the size for "/matchSize" route"""

    data = pandas_db.Products("name")
    try:
        return fl.jsonify({
           "ok_size": data.match_size().to_dict()
        })
    except KeyError:
        return data.error


def search_by_color_q():
    """Function that search all products
    by color for the "/search?color=" route"""

    data = pandas_db.Products("name")
    try:
        return fl.jsonify({
            "right_color": data.search_by_col(fl.request.args.get("color")).to_dict()
        })
    except KeyError:
        return data.error


def count_reviews():
    """Function that count all reviews
    for a product for the "/search?q=" route"""

    data = pandas_db.Products()
    try:
        return fl.jsonify({
           "count_review": data.count_rev()
        })
    except KeyError:
        return data.error
