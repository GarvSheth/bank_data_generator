from generators.users import generate_users
from generators.devices import generate_devices
from generators.merchants import generate_merchants
from generators.locations import generate_locations

print("Generating Users...")
users = generate_users()
users.to_csv("output/users.csv", index=False)

print("Generating Devices...")
devices = generate_devices(users)
devices.to_csv("output/devices.csv", index=False)

print("Generating Merchants...")
merchants = generate_merchants()
merchants.to_csv("output/merchants.csv", index=False)

print("Generating Locations...")
locations = generate_locations()
locations.to_csv("output/locations.csv", index=False)


print("\nDataset Generation Complete!")
print(f"Users        : {len(users)}")
print(f"Devices      : {len(devices)}")
print(f"Merchants    : {len(merchants)}")
print(f"Locations    : {len(locations)}")