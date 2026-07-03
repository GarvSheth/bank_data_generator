import random
import uuid

import pandas as pd
from faker import Faker

from config import NUM_MERCHANTS

fake = Faker("en_IN")
random.seed(42)

MERCHANT_CATEGORIES = {

    "E-Commerce": (
        [
            "Amazon",
            "Flipkart",
            "Myntra",
            "Ajio"
        ],
        (500,50000)
    ),

    "Grocery": (
        [
            "BigBasket",
            "Blinkit",
            "Zepto",
            "DMart"
        ],
        (100,8000)
    ),

    "Fuel": (
        [
            "Indian Oil",
            "HP",
            "BPCL",
            "Shell"
        ],
        (500,7000)
    ),

    "Travel": (
        [
            "IRCTC",
            "Uber",
            "Ola",
            "MakeMyTrip"
        ],
        (300,50000)
    ),

    "Healthcare": (
        [
            "Apollo",
            "Fortis",
            "MedPlus"
        ],
        (500,100000)
    ),

    "Restaurant": (
        [
            "Swiggy",
            "Zomato",
            "Dominos",
            "McDonalds"
        ],
        (100,5000)
    ),

    "Entertainment": (
        [
            "Netflix",
            "Spotify",
            "BookMyShow"
        ],
        (100,20000)
    ),

    "Luxury": (
        [
            "Rolex",
            "Louis Vuitton",
            "Gucci",
            "Apple Store"
        ],
        (5000,500000)
    )
}

COUNTRIES = [
    "India",
    "USA",
    "UK",
    "Germany",
    "Singapore",
    "UAE",
    "Australia"
]

RISK_LEVEL = {
    "Low": (0.00,0.30),
    "Medium": (0.31,0.70),
    "High": (0.71,1.00)
}


def merchant_risk():

    p = random.random()

    if p < 0.80:

        level = "Low"

    elif p < 0.95:

        level = "Medium"

    else:

        level = "High"

    low,high = RISK_LEVEL[level]

    return level, round(random.uniform(low,high),2)


def generate_merchant(i):

    category = random.choice(
        list(MERCHANT_CATEGORIES.keys())
    )

    merchants,txn_range = MERCHANT_CATEGORIES[category]

    level,risk = merchant_risk()

    return {

        "MerchantID": f"MER{i:06d}",

        "MerchantName":
            random.choice(merchants)
            + " "
            + str(random.randint(1,500)),

        "Category": category,

        "Country": random.choice(COUNTRIES),

        "City": fake.city(),

        "MerchantAgeYears":
            random.randint(1,25),

        "Verified":
            random.random() < 0.95,

        "MerchantRiskLevel":
            level,

        "MerchantRiskScore":
            risk,

        "ChargebackRate":
            round(random.uniform(0,8),2),

        "AverageTransaction":
            random.randint(
                txn_range[0],
                txn_range[1]
            ),

        "FraudHistory":
            random.randint(0,50),

        "Rating":
            round(random.uniform(2.5,5),1)
    }


def generate_merchants():

    merchants=[]

    for i in range(1,NUM_MERCHANTS+1):

        merchants.append(
            generate_merchant(i)
        )

    return pd.DataFrame(merchants)


if __name__=="__main__":

    df=generate_merchants()

    df.to_csv(
        "output/merchants.csv",
        index=False
    )

    print(df.head())

    print()

    print(
        f"Generated {len(df)} merchants."
    )