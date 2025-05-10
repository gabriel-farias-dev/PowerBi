import logging.config
from datetime import datetime as dt, timedelta
import random
import pandas as pd
import numpy as np
from faker import Faker
import logging
import psycopg2
import os
# from secrets_psql import HOST,PASSWORD

############ Preparation 

#Logs Directory
os.makedirs(r'../../Logs',exist_ok=True)

#Log
logging.basicConfig(filename=r"../../Logs/TO_generation.log")

#Faker
fake = Faker()

# Branchs, products, dates e etc
transp_id = 0
branchs = ['SP','RJ','DF','RS','RN','AM','CE','PA','MG','MGR','MGRS','GO','PR','ES']

products_by_category = {
    "Móveis": [
        'Cadeira', 'Mesa', 'Sofá', 'Cama', 'Armário', 'Estante', 'Poltrona', 'Guarda-roupa',
        'Luminária', 'Cômoda', 'Mesa de cabeceira', 'Prateleira', 'Rack', 'TV', 'Aparador',
        'Balcão', 'Cortina', 'Tapete', 'Quadro', 'Espelho'
    ],
    "Eletrodomésticos": [
        'Banheira', 'Vaso sanitário', 'Lavabo', 'Chuveiro', 'Espremedor de frutas', 'Cafeteira',
        'Liquidificador', 'Geladeira', 'Fogão', 'Micro-ondas', 'Ar condicionado', 'Ventilador',
        'Exaustor', 'Freezer', 'Batedeira', 'Cortador de grama', 'Secadora de roupas',
        'Máquina de lavar', 'Ferro de passar', 'Aspirador de pó'
    ],
    "Eletrônicos": [
        'Notebook', 'Smartphone', 'Tablet', 'Relógio', 'Fone de ouvido', 'Televisor', 'Projetor',
        'Impressora', 'Computador', 'Câmera fotográfica', 'Roteador', 'Caixa de som',
        'Console de videogame'
    ],
    "Vestuário e Acessórios": [
        'Tênis', 'Bota', 'Sandália', 'Sapato', 'Chinelo', 'Jaqueta', 'Camisa', 'Calça',
        'Short', 'Saia', 'Vestido', 'Blusa', 'Cachecol', 'Boné', 'Óculos', 'Bolsa',
        'Carteira', 'Cinto', 'Mochila', 'Relógio de pulso', 'Colar', 'Anel', 'Brincos', 'Pulseira'
    ]
}

sections = ['001','002','003','004','005','006','007','008','009','010','011','012','013']
users = []
dataList = []

for i in range(50):
    users.append(fake.unique.name())

ty_trans = {
    1:{
        'origin':['001','002','003','004'],
        'destiny':'009'
    },
    2:{
        'origin':['001','002','003','004'],
        'destiny':['005','006','007','008']
    },
    3:{
        'origin':'009',
        'destiny':['010','011','012','013']
    },
    3:{
        'origin':'009',
        'destiny':['001','002','003','004']
    }
}

def processMovi(hourAdd: int,branch: str,day:int,ttrasn:int,transp_id:int, hourlimit:int = 0,unitReturn:int = 1) -> list:
    #Down
    today = (dt.now() - timedelta(days=day)).strftime('%Y-%m-%d')
    hour = int(round((random.random() * hourAdd) + hourlimit, 0))
    minute = int(round(random.random() * 59, 0))
    sec =  int(round(random.random() * 59, 0))

    #We need to discover if origin or destiny is list or unique value
    if type(ty_trans[ttrasn]['origin']) == list:
        dep_ori = int(random.choice(ty_trans[ttrasn]['origin']))
    else:
        dep_ori = int(ty_trans[ttrasn]['origin'])
    
    if type(ty_trans[ttrasn]['destiny']) == list:
        dep_dest = int(random.choice(ty_trans[ttrasn]['destiny']))
    else:
        dep_dest = int(ty_trans[ttrasn]['destiny'])

    category = random.choice(list(products_by_category.keys()))
    product = random.choice(products_by_category[category])
    unit = int(round(random.randint(1,2000) * unitReturn,0))
    user = random.choice(users)

    return [transp_id,branch,today,f'{hour}:{minute}:{sec}',category,product,ttrasn,dep_ori,dep_dest,unit,user]


############### Development of the base
print('Generation the data ...')
for everyBranch in branchs:
    for everyDay in range(-390,0):
        for everyTrasn in range(0, random.randint(25,350)):
            transp_id =transp_id + 1
            dataList.append(processMovi(hourAdd=12,branch=everyBranch,day=everyDay,ttrasn=1,transp_id=transp_id))
            transp_id =transp_id + 1
            dataList.append(processMovi(hourAdd=4,hourlimit=12,branch=everyBranch,day=everyDay,ttrasn=3,transp_id=transp_id))
            
            #return?
            returnUnit = random.choices([True,False],[0.3,0.7],k=1)[0]
            if returnUnit:
                transp_id =transp_id + 1
                dataList.append(processMovi(hourAdd=4,hourlimit=12,branch=everyBranch,day=everyDay,ttrasn=2,transp_id=transp_id,unitReturn= random.random() ))


print('Saving ...')
df = pd.DataFrame(dataList,columns=['id','branch','date','hour','categoria','produto','move_id','dep_origem','dep_destiny','units','user'])


if not os.path.exists(r'../../DataToInsert'):
    os.mkdir(r'../../DataToInsert')

connection = psycopg2.connect(f'dbname=db_logistica user= password=')
cursor = connection.cursor()

date = dt.now().strftime('%Y-%m-%d')
df.to_csv(os.path.join(r'../../DataToInsert',f'transp_{date}.csv'),index=None,sep=';')

print('Import data in the database ...')
#Inserindo
cursor.execute('truncate table fact.FT_TRANSPORT')
cursor.execute(f"COPY FACT.FT_TRANSPORT FROM '{os.path.join(r'C:\Users\Farias\Desktop\PowerBi\DataToInsert',f'transp_{date}.csv')}' (FORMAT 'csv',header,delimiter ';')");
connection.commit()
print('inserindo com sucesso')

print('Success')
