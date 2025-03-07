import json
from logging import getLogger

import flask as fl

import services
from config_data import Products


logger = getLogger(__name__)


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

    data = Products(new_index="text")

    try:
        return fl.jsonify({
            "pos_review": services.get_all_pos_rev(products=data)
        })
    except KeyError:
        logger.error("Использованна неправильная колонна в методе set_index => Страница не открылась.")


def get_positive_review(page):
    """Function that displays positive
    reviews for the "/positive/page" route

    Parameters:
    1. page - the page number with reviews"""

    data = Products(new_index="text")
    page = int(page)

    try:
        return fl.jsonify({
            "pos_review": services.get_pos_rev(products=data, page=page)
        })
    except KeyError:
        logger.error("Использованна неправильная колонна в методе set_index => Страница не открылась.")


def get_all_negative_review():
    """Function that displays all positive
     reviews for the "/negative" route"""

    data = Products(new_index="text")

    try:
        return fl.jsonify({
            "neg_review": services.get_all_neg_rev(products=data)
        })
    except KeyError:
        logger.error("Использованна неправильная колонна в методе set_index => Страница не открылась.")


def get_negative_review(page):
    """Function that displays negative reviews for the "/positive/page" route

    Parameters:
    1. page - the page number with reviews"""

    data = Products(new_index="text")
    page = int(page)

    try:
        return fl.jsonify({
            "neg_review": services.get_neg_rev(products=data, page=page)
        })
    except KeyError:
        logger.error("Использованна неправильная колонна в методе set_index => Страница не открылась.")


def search_by_keyword_q():
    """Function that search all products
    by word for the "/search?q=" route"""

    data = Products(new_index="name")

    try:
        return fl.jsonify({
            "results": services.search_by_word(
                products=data, word=fl.request.args.get("q"))
        })
    except KeyError:
        logger.error("Использованна неправильная колонна в методе set_index => Страница не открылась.")


def get():
    """Function that displays an HTML page with
    buyer reviews for a POST request"""

    if fl.request.method == "POST":
        json_object = fl.request.form["JSON"]
        json_obj = json.loads(json_object)
        # json_obj = fl.request.json       |postman|
        data = Products(new_index="name")

        try:
            return services.get_buyer_rev(
                products=data,
                reviewer_name=json_obj["reviewerName"],
                product=json_obj["name"]
            ).to_dict()
        except KeyError:
            pass
    else:
        return fl.render_template("get.html")


def get_mean_product_mark_q():
    """Function that displays the average rating
    of a product by name for "/product" route """

    data = Products()

    return fl.jsonify({
        "means": [services.get_mean_product(
            products=data, word=fl.request.args.get("name"))]
        })


def match_size():
    """Function that displays products that are in stock
    and fit the size for "/matchSize" route"""

    data = Products(new_index="name")

    try:
        return fl.jsonify({
           "ok_size": services.match_size(products=data)
        })
    except KeyError:
        logger.error("Использованна неправильная колонна в методе set_index => Страница не открылась.")


def search_by_color_q():
    """Function that search all products
    by color for the "/search?color=" route"""

    data = Products(new_index="name")

    try:
        return fl.jsonify({
            "right_color": services.search_by_col(
                products=data, color=fl.request.args.get("color"))
        })
    except KeyError:
        logger.error("Использованна неправильная колонна в методе set_index => Страница не открылась.")


def count_reviews():
    """Function that count all reviews
    for a product for the "/search?q=" route"""

    data = Products()

    try:
        return fl.jsonify({
           "count_review": services.count_rev(products=data)
        })
    except KeyError:
        logger.error("Использованна неправильная колонна в методе set_index => Страница не открылась.")
