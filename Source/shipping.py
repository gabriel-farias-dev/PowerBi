import pandas as pd
from datetime import datetime as dt,timedelta
import csv
import os
import psycopg2
import random
from faker import Faker
from secrets_psql import HOST,PASSWORD
import logging as log

# 3 datasets will be created
# Clients DataSet

def clients(NofClients:int) -> pd.DataFrame:
    """Send a number of clients that will be generate and return 
    a DataFrame with clients names and address"""
    
    clients_list = []
    fake = Faker('pt-BR')
    
    for _ in range(0,NofClients):
        clients_list.append([fake.name(),fake.address()])
        
    df_clients = pd.DataFrame(data=clients_list,columns=['Company_Name','Company_Address'])
    
    return df_clients

def branchs() -> pd.DataFrame:
    """Return 14 branchs with address"""
    fake = Faker('pt-BR')
    branch_list = []
    branchs = ['Blue','Yellow','Red','DeepBlue','Green','Purple','Pink','Orange','Brown','White','Black','Gray','Magenta','Cyan']
    
    for everyBranch in branchs:
        branch_list.append([everyBranch,fake.address()])
       
    df_branchs = pd.DataFrame(data=branch_list,columns=['Branch_Name','Branch_Address'])
    
    return df_branchs
    
    
def fact_shipping():
    fake = Faker('pt-BR')
    df_branch = branchs()
    
    status = ['Not Started','In Transit','Strategic Stop','Heading to Final Destination','Completed']
    
    for index_bra,everyBranch in df_branch.iterrows():
        df_clients = clients(random.randint(0,25))
        
        for index_cli,everyClient in df_clients.iterrows():
            #status_delivery = random.choice(status)
            status_delivery = 'Not Started'
            if status_delivery == 'Not Started':
                stops = 0
                last_local = everyBranch['Branch_Address']
                driver_name = fake.name()
                quant_boxes = random.randint(2,5) * len(df_clients)
                print([everyBranch['Branch_Name'],everyClient['Company_Name'],stops,last_local,driver_name,quant_boxes,everyClient['Company_Address']])
                exit()
                
        
        #for everyDay in range(0,365):
         #   snapshot = (dt.now() - timedelta(days=everyDay)).strftime('%Y-%m-%d')
         
fact_shipping()