import pandas as pd


api_db = pd.read_csv("prepared_data.csv", sep=",")


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

    def search_by_col(self, color):
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
