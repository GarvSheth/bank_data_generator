import random
import uuid
import hashlib
from datetime import datetime

import pandas as pd
from faker import Faker

from users import generate_users

fake = Faker("en_IN")
random.seed(42)

DEVICE_TYPES = {
    "Android": [
        "Samsung Galaxy S24",
        "Google Pixel 9",
        "OnePlus 12",
        "Xiaomi 14",
        "Nothing Phone 2"
    ],

    "iPhone": [
        "iPhone 13",
        "iPhone 14",
        "iPhone 15",
        "iPhone 16"
    ],

    "Laptop": [
        "MacBook Air M3",
        "MacBook Pro",
        "Dell XPS 15",
        "HP Spectre",
        "Lenovo ThinkPad"
    ],

    "Tablet": [
        "iPad Air",
        "Galaxy Tab S9",
        "OnePlus Pad"
    ]
}

BROWSERS = [
    "Chrome",
    "Safari",
    "Firefox",
    "Edge"
]

APP_VERSION = [
    "1.0.0",
    "1.1.2",
    "2.0.1",
    "2.3.4",
    "3.0.0"
]


def create_fingerprint():

    return hashlib.sha256(
        uuid.uuid4().hex.encode()
    ).hexdigest()


def generate_device(device_no, user_id):

    device_type = random.choice(list(DEVICE_TYPES.keys()))

    model = random.choice(
        DEVICE_TYPES[device_type]
    )

    trusted = random.random() < 0.9

    rooted = False

    if device_type == "Android":
        rooted = random.random() < 0.05

    emulator = random.random() < 0.01

    return {

        "DeviceID": f"DEV{device_no:07d}",

        "UserID": user_id,

        "DeviceType": device_type,

        "Model": model,

        "OperatingSystem": device_type,

        "OSVersion": f"{random.randint(11,18)}.{random.randint(0,5)}",

        "Browser": random.choice(BROWSERS),

        "AppVersion": random.choice(APP_VERSION),

        "Trusted": trusted,

        "Rooted": rooted,

        "Emulator": emulator,

        "Fingerprint": create_fingerprint(),

        "FirstSeen": fake.date_between(
            start_date="-5y",
            end_date="-2y"
        ),

        "LastSeen": fake.date_between(
            start_date="-30d",
            end_date="today"
        )
    }


def generate_devices(users_df):

    devices = []

    device_counter = 1

    for _, user in users_df.iterrows():

        num_devices = random.randint(1,3)

        for _ in range(num_devices):

            devices.append(

                generate_device(
                    device_counter,
                    user["UserID"]
                )

            )

            device_counter += 1

    return pd.DataFrame(devices)


if __name__ == "__main__":

    users = generate_users()

    devices = generate_devices(users)

    devices.to_csv(
        "output/devices.csv",
        index=False
    )

    print(devices.head())

    print()

    print(f"Generated {len(devices)} devices.")