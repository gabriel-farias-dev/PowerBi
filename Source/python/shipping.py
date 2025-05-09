import pandas as pd
import random
from faker import Faker
from datetime import datetime as dt, timedelta

# 3 datasets will be created
# Clients DataSet

list_final = []

def clients(NofClients: int) -> pd.DataFrame:
    """Send a number of clients that will be generated and return 
    a DataFrame with client names and address (latitude and longitude)."""
    
    clients_list = []
    fake = Faker('pt-BR')
    
    for _ in range(NofClients):
        lat, lng = fake.latlng()
        clients_list.append([fake.name(), lat, lng])
        
    df_clients = pd.DataFrame(data=clients_list, columns=['Company_Name', 'Latitude', 'Longitude'])
    return df_clients

def branchs() -> pd.DataFrame:
    """Return 14 branches with latitude and longitude."""
    fake = Faker('pt-BR')
    branch_list = []
    branch_names = ['Blue', 'Yellow', 'Red', 'DeepBlue', 'Green', 'Purple', 'Pink', 'Orange', 'Brown', 'White', 'Black', 'Gray', 'Magenta', 'Cyan']
    
    for branch_name in branch_names:
        lat, lng = fake.latlng()
        branch_list.append([branch_name, lat, lng])
       
    df_branches = pd.DataFrame(data=branch_list, columns=['Branch_Name', 'Latitude', 'Longitude'])
    return df_branches
    
def fact_shipping():
    """Generate the shipping fact table."""
    fake = Faker('pt-BR')
    df_branch = branchs()
    
    status = ['Not Started', 'In Transit', 'Strategic Stop', 'Heading to Final Destination', 'Completed']
    
    for _, everyBranch in df_branch.iterrows():
        df_clients = clients(random.randint(50, 125))
        
        for _, everyClient in df_clients.iterrows():
            status_delivery = random.choice(status)
            driver_name = fake.name()
            quant_boxes = random.randint(2, 5) * len(df_clients)
            
            if status_delivery == 'Not Started' or status_delivery == 'In Transit':
                stops = 0
                last_local_lat, last_local_long = everyBranch['Latitude'], everyBranch['Longitude']
                
            elif status_delivery == 'Strategic Stop':
                stops = 1
                last_local_lat, last_local_long = fake.latlng()
                
            elif status_delivery == 'Heading to Final Destination' or status_delivery == 'Completed':
                stops = random.randint(1, 3)
                last_local_lat, last_local_long = fake.latlng()
                
            list_final.append([
                everyBranch['Branch_Name'], everyClient['Company_Name'],
                stops, last_local_lat, last_local_long, driver_name,
                quant_boxes, everyClient['Latitude'], everyClient['Longitude']
            ])

    # Convert to DataFrame
    columns = [
        'Branch_Name', 'Company_Name', 'Stops', 'Last_Latitude', 'Last_Longitude', 
        'Driver_Name', 'Quantity_Boxes', 'Client_Latitude', 'Client_Longitude'
    ]
    df_fact_shipping = pd.DataFrame(list_final, columns=columns)
    return df_fact_shipping, df_clients, df_branch

# Generate the data
df_fact, df_client, df_branch = fact_shipping()