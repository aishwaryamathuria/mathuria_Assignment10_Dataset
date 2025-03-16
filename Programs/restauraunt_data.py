import random
import pandas as pd
from datetime import datetime, timedelta

# Define the resources and other variables
resources = {
    "receptionist": ["receptionist1", "receptionist2", "receptionist3"],
    "tables": ['1', '2', '3', '4', '5', '6'],
    "waiter": ['waiter1', 'waiter2', 'waiter3'],
    "chef": ['chef1', 'chef2']
}

delays = {
    "receptionist": timedelta(minutes=random.randint(6, 10)),
    "tables": 1,
    "waiter": timedelta(minutes=random.randint(6, 10)),
    "chef": timedelta(minutes=random.randint(6, 10))
}

locations = ["reception", "main dining", "kitchen"]

menu_items = {
    1: {"description": "Burger", "type": "food", "price": 1200},
    2: {"description": "Pizza", "type": "food", "price": 1500},
    3: {"description": "Salad", "type": "food", "price": 900},
    7: {"description": "Steak", "type": "food", "price": 2500},
    8: {"description": "Pasta", "type": "food", "price": 1300},
    9: {"description": "Ice Cream", "type": "dessert", "price": 600},
    10: {"description": "Soda", "type": "beverage", "price": 300},
    11: {"description": "Beer", "type": "beverage", "price": 500},
    12: {"description": "Wine", "type": "beverage", "price": 800},
}

activities = ["Greeted", "Seated", "Ordered", "Prepared", "Served", "Paid"]

# Function to generate random data for a simulation
def generate_event_log(num_events):
    log = []
    
    # Starting timestamp for the simulation
    start_time = datetime(2025, 3, 16, 8, 0, 0)
    
    # Dictionary to track resource availability
    resource_availability = {
        "receptionist": [],
        "waiter": [],
        "chef": []
    }
    
    # List to keep track of active cases
    active_cases = []
    
    # Generate event logs for multiple customers
    for event_id in range(1, num_events + 1):
        # Random customer/dining party
        case_id = event_id
        
        # Random party size between 1 and 6
        party_size = random.randint(1, 6)
        
        # Randomly generate the arrival timestamp (overlap with other events)
        timestamp = start_time + timedelta(minutes=random.randint(6, 10))  # Allow some overlap with other customers
        start_time = timestamp
        
        # Each customer goes through activities, but activities can overlap with others
        case_events = []
        
        for activity in activities:
            # Get the assigned resource and location for the current activity
            resource_type, resource, location = assign_resource_for_activity(activity, timestamp, resource_availability)
            
            # Generate random menu items for the order if it's the "Ordered" activity
            if activity == "Ordered":
                order_items = random.sample(list(menu_items.keys()), random.randint(1, len(menu_items.keys())))
                order_item_descriptions = [menu_items[item]["description"] for item in order_items]
                order_item_types = [menu_items[item]["type"] for item in order_items]
                order_size = len(order_items)
                order_item_prices = [menu_items[item]["price"] for item in order_items]
                
                # Calculate total bill, tax, and tip
                bill_for_items = sum(order_item_prices)
                bill_tax = int(bill_for_items * 0.10)  # Assuming 10% tax
                bill_tip = int(bill_for_items * 0.15)  # Assuming 15% tip
            else:
                order_items = order_item_descriptions = order_item_types = order_size = order_item_prices = bill_for_items = bill_tax = bill_tip = None
            
            # Create the event for this activity
            event = {
            	"scenario": "scenario1",
                "caseID": "1_" + str(case_id),
                "timestamp": timestamp,
                "activity": activity,
                "resource": resource,
                "resource_type": resource_type,
                "location": location,
                "party_size": party_size,
                "order_items": order_items,
                "order_item_descriptions": order_item_descriptions,
                "order_item_types": order_item_types,
                "order_size": order_size,
                "order_item_prices": order_item_prices,
                "bill_for_items": bill_for_items,
                "bill_tax": bill_tax,
                "bill_tip": bill_tip
            }
            
            # Append the event to the case
            case_events.append(event)
            
            # Update the timestamp for the next activity within the case, allowing overlap
            timestamp = timestamp + timedelta(minutes=random.randint(1, delays[resource_type]))  # Random overlap for next activity
        
        # Add all events for this customer to the log
        log.extend(case_events)
        
    df = pd.DataFrame(log)
    return df

# Function to assign resources and ensure availability for the given activity
def assign_resource_for_activity(activity, timestamp, resource_availability):
    if activity == "Greeted":
        resource_type = "receptionist"
        resource = get_available_resource(resource_type, timestamp, resource_availability)
        location = "reception"
    if activity == "Seated":
        resource_type = "tables"
        resource = get_available_resource(resource_type, timestamp, resource_availability)
        location = "reception"
    elif activity == "Ordered":
        resource_type = "waiter"
        resource = get_available_resource(resource_type, timestamp, resource_availability)
        location = "main dining"
    elif activity == "Prepared":
        resource_type = "chef"
        resource = get_available_resource(resource_type, timestamp, resource_availability)
        location = "kitchen"
    elif activity == "Served":
        resource_type = "waiter"
        resource = get_available_resource(resource_type, timestamp, resource_availability)
        location = "main dining"
    elif activity == "Paid":
        resource_type = "waiter"
        payment_delay=timedelta(minutes=random.randint(6, 10))
        resource = get_available_resource(resource_type, timestamp, resource_availability, payment_delay)
        location = "main dining"
    
    return resource_type, resource, location

# Function to get an available resource
def get_available_resource(resource_type, timestamp, resource_availability, payment_delay=timedelta(minutes=0)):
    # Get a list of resources for the given type
    available_resources = resources[resource_type]
    
    # Check for availability - if all resources are occupied, we delay the task
    for resource in available_resources:
        # Check if the resource is currently available
        if resource not in resource_availability or resource_availability[resource] <= timestamp:
            # Resource is available, assign it and update its availability time
            resource_availability[resource] = timestamp + timedelta(minutes=delays[resource_type])
            return resource
    
    # If no resources are available, delay the task by 10 minutes and retry
    delay_time = timestamp + timedelta(minutes=10)
    return get_available_resource(resource_type, delay_time, resource_availability)

# Generate data with and without robots
df = generate_event_log(200)
df.to_csv('restaurant_data.csv', index=False)
print("Data generation complete. CSV files saved.")

output_table = pd.concat([df], ignore_index=True, sort=False)
