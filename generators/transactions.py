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

# Faster lookups

user_list = users.to_dict("records")

merchant_list = merchants.to_dict("records")

location_list = locations.to_dict("records")

device_lookup = {}

for user_id, group in devices.groupby("UserID"):
    device_lookup[user_id] = group.to_dict("records")

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
    user = random.choice(user_list)
    user_id = user["UserID"]

    # Devices owned by this user
    device = random.choice(
        device_lookup[user_id]
    )

    # Random Merchant
    merchant = random.choice(
        merchant_list
    )

    # Random Location
    location = random.choice(
        location_list
    )

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

    # -------------------------
    # Fraud Logic
    # -------------------------

    risk = 0

    is_new_device = False
    is_new_location = False

    # Very high transaction
    if amount > avg_amount * 5:
        risk += 40

    # New device
    if random.random() < 0.10:
        is_new_device = True
        risk += 25

    # New location
    if random.random() < 0.08:
        is_new_location = True
        risk += 20

    # High-risk merchant
    if merchant["MerchantRiskLevel"] == "High":
        risk += 20

    elif merchant["MerchantRiskLevel"] == "Medium":
        risk += 10

    # High-risk country
    if location["RiskLevel"] == "High":
        risk += 20

    elif location["RiskLevel"] == "Medium":
        risk += 10

    # Previous frauds
    risk += user["PreviousFraudCount"] * 15

    # Credit score
    if user["CreditScore"] < 550:
        risk += 15

    # Final decision
    is_fraud = risk >= 60

    timestamp = fake.date_time_between(
        start_date="-1y",
        end_date="now"
    )

    return {
        "TransactionID": f"TXN{uuid.uuid4().hex[:12].upper()}",
        "CreditScore": user["CreditScore"],
        "PreviousFraudCount": user["PreviousFraudCount"],
        "UserID": user_id,
        "MerchantID": merchant["MerchantID"],
        "MerchantCategory": merchant["Category"],
        "MerchantRisk": merchant["MerchantRiskLevel"],
        "DeviceType": device["DeviceType"],
        "City": location["City"],
        "Country": location["Country"],
        "LocationRisk": location["RiskLevel"],
        "Amount": amount,
        "TransactionType": random.choice(TRANSACTION_TYPES),
        "Timestamp": timestamp,
        "HourOfDay": timestamp.hour,
        "DayOfWeek": timestamp.strftime("%A"),
        "PreviousBalance": previous_balance,
        "CurrentBalance": current_balance,
        "RiskScore": risk,
        "IsNewDevice": is_new_device,
        "IsNewLocation": is_new_location,
        "FraudLabel": int(is_fraud)
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

print("\nFraud Distribution:")

print(transactions_df["FraudLabel"].value_counts())

print()

print(
    transactions_df["FraudLabel"].value_counts(normalize=True) * 100
)

print(transactions_df.head())

print()

print(f"Generated {len(transactions_df)} transactions.")