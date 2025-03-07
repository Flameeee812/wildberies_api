def get_all_pos_rev(products):
    return products.new_index_data["mark"][products.new_index_data["mark"] > 3].to_dict()


def get_pos_rev(products, page):
    products = products.new_index_data["mark"][products.new_index_data["mark"] > 3]
    sliced_products = products[(100 * (page - 1)):(100 * page)]

    return sliced_products.to_dict()


def get_all_neg_rev(products):
    return products.new_index_data["mark"][products.new_index_data["mark"] <= 3].to_dict()


def get_neg_rev(products, page):
    products = products.new_index_data["mark"][products.new_index_data["mark"] <= 3]
    sliced_products = products[(100 * (page - 1)):(100 * page)]

    return sliced_products.to_dict()


def search_by_word(products, word):
    return products.new_index_data["text"][products.new_index_data["text"].str.contains(word, na=False)].to_dict()


def get_buyer_rev(products, reviewer_name, product):
    filtered_data = products.new_index_data.loc[product]
    return filtered_data[filtered_data["reviewerName"] == reviewer_name]["text"].to_dict()


def search_by_col(products, color):
    return products.new_index_data["color"][products.new_index_data["color"] == color].to_dict()


def match_size(products):
    return products.new_index_data["matchingSize"][
            products.new_index_data["has_sizes"].values & (products.new_index_data["matchingSize"] == "ok")
        ].to_dict()


def get_mean_product(products, word):
    filtered_products = products.new_index_data[products.new_index_data["name"].str.contains(word, na=False)]

    return filtered_products.groupby("name")["mark"].mean().round(1).to_dict()


def count_rev(products):
    return products.new_index_data.groupby("name")["text"].count().to_dict()
