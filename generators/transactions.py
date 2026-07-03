import random
import uuid
from datetime import datetime

import pandas as pd
from faker import Faker

from config import NUM_TRANSACTIONS

fake = Faker("en_IN")
random.seed(42)

# ===========================
# Load CSVs
# ===========================

users = pd.read_csv("output/users.csv")
devices = pd.read_csv("output/devices.csv")
merchants = pd.read_csv("output/merchants.csv")
locations = pd.read_csv("output/locations.csv")

# ===========================
# Transaction Types
# ===========================

TRANSACTION_TYPES = [
    "UPI",
    "Debit Card",
    "Credit Card",
    "Net Banking",
    "Wallet"
]

# ===========================
# User Balances
# ===========================

user_balance = {}

for _, user in users.iterrows():

    income = user["AnnualIncome"]

    balance = random.randint(
        int(income * 0.5),
        int(income * 2)
    )

    user_balance[user["UserID"]] = balance

# =========================================
# ADD STEP 7 HERE (generate_transaction())
# =========================================

def generate_transaction():

    # Random User
    user = users.sample(1).iloc[0]
    user_id = user["UserID"]

    # Devices owned by this user
    user_devices = devices[
        devices["UserID"] == user_id
    ]

    device = user_devices.sample(1).iloc[0]

    # Random Merchant
    merchant = merchants.sample(1).iloc[0]

    # Random Location
    location = locations.sample(1).iloc[0]

    previous_balance = user_balance[user_id]

    # Average spending of user
    avg_amount = user["AverageTransactionAmount"]

    amount = max(
        1,
        random.randint(
            max(1, int(avg_amount * 0.5)),
            max(2, int(avg_amount * 2))
        )
    )

    # Don't allow negative balance
    amount = min(amount, previous_balance)

    current_balance = previous_balance - amount

    user_balance[user_id] = current_balance

    return {
        "TransactionID": str(uuid.uuid4()),
        "UserID": user_id,
        "MerchantID": merchant["MerchantID"],
        "DeviceID": device["DeviceID"],
        "LocationID": location["LocationID"],
        "Amount": amount,
        "TransactionType": random.choice(TRANSACTION_TYPES),
        "Timestamp": fake.date_time_between(
            start_date="-1y",
            end_date="now"
        ),
        "PreviousBalance": previous_balance,
        "CurrentBalance": current_balance,
        "IsNewDevice": False,
        "IsNewLocation": False,
        "FraudLabel": 0
    }

# =========================================
# Testing
# =========================================

transactions = []

for _ in range(NUM_TRANSACTIONS):
    transactions.append(generate_transaction())

transactions_df = pd.DataFrame(transactions)

transactions_df.to_csv(
    "output/transactions.csv",
    index=False
)

print(transactions_df.head())

print()

print(f"Generated {len(transactions_df)} transactions.")