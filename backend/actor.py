import pandas as pd

def lookup_product(product):

    df = pd.read_csv(
        "data/prices.csv"
    )

    row = df[
        df["product"].str.lower()
        ==
        product.lower()
    ]

    if len(row):

        return row.iloc[0].to_dict()

    return None