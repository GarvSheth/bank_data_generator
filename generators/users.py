import random
import uuid
from datetime import datetime

import numpy as np
import pandas as pd
from faker import Faker

from config import NUM_USERS

fake = Faker("en_IN")
random.seed(42)
np.random.seed(42)

occupations = {
    "Student": (18, 25, (0, 300000)),
    "Software Engineer": (22, 45, (600000, 2500000)),
    "Doctor": (28, 65, (1000000, 5000000)),
    "Teacher": (24, 60, (400000, 1200000)),
    "Business Owner": (25, 70, (1000000, 10000000)),
    "Lawyer": (25, 65, (800000, 4000000)),
    "Government Employee": (23, 60, (500000, 1800000)),
    "Freelancer": (21, 55, (300000, 3000000)),
    "Accountant": (23, 60, (500000, 2000000)),
    "Consultant": (25, 60, (800000, 5000000)),
    "Manager": (25, 60, (800000, 3500000)),
    "Designer": (21, 50, (300000, 2000000)),
    "Retired": (60, 80, (200000, 1000000))
}

payment_methods = [
    "UPI",
    "Credit Card",
    "Debit Card",
    "Net Banking",
    "Wallet"
]


def generate_credit_score(income):
    """
    Higher income -> slightly better credit score
    """

    score = int(np.random.normal(700, 70))

    if income > 2500000:
        score += random.randint(20, 60)

    elif income < 400000:
        score -= random.randint(10, 40)

    return max(300, min(score, 900))


def generate_user(user_no):

    occupation = random.choice(list(occupations.keys()))

    age_min, age_max, income_range = occupations[occupation]

    age = random.randint(age_min, age_max)

    income = random.randint(
        income_range[0],
        income_range[1]
    )

    credit_score = generate_credit_score(income)

    account_age = random.randint(1, 120)

    previous_fraud = np.random.choice(
        [0, 1, 2],
        p=[0.95, 0.04, 0.01]
    )

    risk_score = round(
        random.uniform(0.05, 0.25),
        2
    )

    if credit_score < 550:
        risk_score += 0.25

    if previous_fraud > 0:
        risk_score += 0.35

    risk_score = min(risk_score, 1.0)

    avg_txn = round(
        income * random.uniform(0.002, 0.02),
        2
    )

    return {

        "UserID": f"USR{user_no:06d}",

        "Name": fake.name(),

        "Email": fake.email(),

        "Phone": fake.phone_number(),

        "Gender": random.choice(["Male", "Female"]),

        "Age": age,

        "Occupation": occupation,

        "AnnualIncome": income,

        "CreditScore": credit_score,

        "RiskScore": risk_score,

        "KYCVerified": random.choice([True, True, True, False]),

        "AccountAgeMonths": account_age,

        "PreviousFraudCount": previous_fraud,

        "AverageTransactionAmount": avg_txn,

        "PreferredPaymentMethod": random.choice(payment_methods),

        "CreatedAt": fake.date_between(
            start_date="-10y",
            end_date="-1d"
        )
    }


def generate_users():

    users = []

    for i in range(1, NUM_USERS + 1):
        users.append(generate_user(i))

    df = pd.DataFrame(users)

    return df


if __name__ == "__main__":

    df = generate_users()

    df.to_csv(
        "output/users.csv",
        index=False
    )

    print(df.head())

    print()

    print(f"Generated {len(df)} users.")