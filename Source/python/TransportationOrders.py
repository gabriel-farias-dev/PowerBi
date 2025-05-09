import logging.config
from datetime import datetime as dt, timedelta
import random
import pandas as pd
import numpy as np
from faker import Faker
import logging
# import psycopg2
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

############### Development of the base
for everyBranch in branchs:
    for everyDay in range(-390,0):

        #Down
        today = (dt.now() - timedelta(days=everyDay)).strftime('%Y-%m-%d')
        hour = round(random.random(0,1) * 12, 0)
        minute = round(random.random(0,1) * 60, 0)
        sec =  round(random.random(0,1) * 60, 0)

        typeTrans = 1
        dep_ori = random.choice(ty_trans[typeTrans]['origin'])
        dep_dest = ty_trans[typeTrans]['destiny']
        category = random.choice(products_by_category.keys())
        product = random.choice(products_by_category[category])
        unit = random.randint(1,2000)
        user = random.choice(users)

        transp_id = transp_id + 1

        dataList.append([transp_id,today,hour + ':' + minute + ':' + sec,category,product,typeTrans,dep_ori,dep_dest,unit,user])

        #ToCubing
        hour = round(random.random(0,1) * 8, 0) + hour
        minute = round(random.random(0,1) * 60, 0)
        sec =  round(random.random(0,1) * 60, 0)

        typeTrans = 3
        dep_ori= ty_trans[typeTrans]['origin']
        dep_dest = random.choice(ty_trans[typeTrans]['destiny'])

        #return?
        returnUnit = random.choice([True,False])
        if returnUnit:
            unit = unit * random.random(0.6,1)
            user = random.choice(users)
        
        transp_id = transp_id + 1
        dataList.append([transp_id,today,hour + ':' + minute + ':' + sec,category,product,typeTrans,dep_ori,dep_dest,unit,user])

        if returnUnit:
            

    
