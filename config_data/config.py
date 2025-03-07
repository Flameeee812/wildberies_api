from dataclasses import dataclass, field

import pandas as pd

from load_csv import products_data


@dataclass
class Products:
    new_index: str = "Unnamed: 0"
    new_index_data: pd.DataFrame = field(init=False)

    def __post_init__(self):
        self.new_index_data = products_data.set_index(self.new_index)
