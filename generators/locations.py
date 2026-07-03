import random
import pandas as pd

random.seed(42)

LOCATIONS = [

    ("India","Delhi","Delhi",28.6139,77.2090,"Asia/Kolkata","Low"),
    ("India","Maharashtra","Mumbai",19.0760,72.8777,"Asia/Kolkata","Low"),
    ("India","Karnataka","Bengaluru",12.9716,77.5946,"Asia/Kolkata","Low"),
    ("India","Tamil Nadu","Chennai",13.0827,80.2707,"Asia/Kolkata","Low"),
    ("India","Telangana","Hyderabad",17.3850,78.4867,"Asia/Kolkata","Low"),
    ("India","West Bengal","Kolkata",22.5726,88.3639,"Asia/Kolkata","Low"),
    ("India","Gujarat","Ahmedabad",23.0225,72.5714,"Asia/Kolkata","Low"),

    ("USA","California","San Francisco",37.7749,-122.4194,"America/Los_Angeles","Medium"),
    ("USA","New York","New York",40.7128,-74.0060,"America/New_York","Medium"),
    ("UK","England","London",51.5072,-0.1276,"Europe/London","Medium"),
    ("Germany","Berlin","Berlin",52.5200,13.4050,"Europe/Berlin","Medium"),
    ("Singapore","Singapore","Singapore",1.3521,103.8198,"Asia/Singapore","Low"),
    ("UAE","Dubai","Dubai",25.2048,55.2708,"Asia/Dubai","Medium"),
    ("Australia","NSW","Sydney",-33.8688,151.2093,"Australia/Sydney","Medium"),

    ("Nigeria","Lagos","Lagos",6.5244,3.3792,"Africa/Lagos","High"),
    ("Russia","Moscow","Moscow",55.7558,37.6173,"Europe/Moscow","High"),
    ("North Korea","Pyongyang","Pyongyang",39.0392,125.7625,"Asia/Pyongyang","High")

]

def risk_score(level):

    if level == "Low":
        return round(random.uniform(0.05,0.30),2)

    elif level == "Medium":
        return round(random.uniform(0.31,0.70),2)

    return round(random.uniform(0.71,1.00),2)


def generate_locations():

    data=[]

    for i,loc in enumerate(LOCATIONS,start=1):

        country,state,city,lat,lon,tz,risk=loc

        data.append({

            "LocationID":f"LOC{i:05d}",

            "Country":country,

            "State":state,

            "City":city,

            "Latitude":lat,

            "Longitude":lon,

            "Timezone":tz,

            "RiskLevel":risk,

            "RiskScore":risk_score(risk),

            "VPNFrequency":random.randint(1,90),

            "FraudCases":random.randint(0,5000)

        })

    return pd.DataFrame(data)


if __name__=="__main__":

    df=generate_locations()

    df.to_csv(
        "output/locations.csv",
        index=False
    )

    print(df.head())

    print()

    print(f"Generated {len(df)} locations.")