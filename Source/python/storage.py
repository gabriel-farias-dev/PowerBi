import pandas as pd
import numpy as np
import time
from datetime import datetime as dt, timedelta as td
import logging as log
from faker import Faker
import random
import psycopg2
import os
from secrets_psql import HOST,PASSWORD

def makingData():
    ################################################### Making Products in WareHouse
    #Variables
    branchs = ['SP','RJ','DF','RS','RN','AM','CE','PA','MG','MGR','MGRS','GO','PR','ES']
    init = time.time()
    products = []
    products_wout_color = ['Cadeira', 'Mesa', 'Sofá', 'Cama', 'Armário', 'Estante', 'Poltrona', 'Guarda-roupa','Luminária', 'Cômoda', 'Mesa de cabeceira', 'Prateleira', 'Rack', 'TV', 'Aparador','Balcão', 'Cortina', 'Tapete', 'Quadro', 'Espelho', 'Banheira', 'Vaso sanitário', 'Lavabo','Chuveiro', 'Espremedor de frutas', 'Cafeteira', 'Liquidificador', 'Geladeira', 'Fogão','Micro-ondas', 'Ar condicionado', 'Ventilador', 'Exaustor', 'Freezer', 'Batedeira','Cortador de grama', 'Secadora de roupas', 'Máquina de lavar', 'Ferro de passar', 'Aspirador de pó','Notebook', 'Smartphone', 'Tablet', 'Relógio', 'Fone de ouvido', 'Televisor', 'Projetor','Impressora', 'Computador', 'Câmera fotográfica', 'Roteador', 'Caixa de som', 'Console de videogame','Tênis', 'Bota', 'Sandália', 'Sapato', 'Chinelo', 'Jaqueta', 'Camisa', 'Calça', 'Short', 'Saia','Vestido', 'Blusa', 'Cachecol', 'Boné', 'Óculos', 'Bolsa', 'Carteira', 'Cinto', 'Mochila','Relógio de pulso', 'Colar', 'Anel', 'Brincos', 'Pulseira']

    # to generate expiration date
    init_vdate = dt(2025,2,28)
    end_vdate = dt(2028,12,31)

    for everyProduct in products_wout_color:
        fake = Faker(['pt_BR'])
        product_color = [f'{everyProduct} {fake.unique.color_name()}' for i in range(15)]
        for everyItem in product_color:
            products.append([everyItem,(dt.now() + td(days=random.randint(0,930))).strftime('%Y-%m-%d')])

    df_item = pd.DataFrame(data=products,columns=['NomeProduto','Validade'])
    print('Created items')
    ###################################################### Making a WareHouse

    #Rooms
    wareHouse_room = [['Receiver',10000],['Receiver',10000],['Stock',50000],['Stock',50000],['Stock',50000],['Stock',50000],['Stock',50000],['Cubing',60000],['Errors',5000],['dispatch',10000],['dispatch',10000],['dispatch',10000],['dispatch',10000]]
    
    df_rooms = pd.DataFrame(data=wareHouse_room,columns=['name','capacity'])
    print('Created WareHouse Rooms')
    

    df_storage = pd.DataFrame()
    snap = dt.now().strftime('%Y-%m-%d %H:%M:%S')
    #storage
    for everyBranch in branchs:
        print(f'Branch: {everyBranch}')
        for everyRoom,row in df_rooms.iterrows():
            for _ in range(0,900):
                
                try:
                    if df_storage[(df_storage['room'] == everyRoom) & (df_storage['branch'] == everyBranch)]['amount'].sum() < row['capacity']:
                        df_transitory = pd.DataFrame([[everyRoom,random.randint(0,len(df_item) - 1),random.randint(0,20),everyBranch,snap]],columns=['room','item','amount','branch','snapshot'])
                        df_storage = pd.concat([df_storage,df_transitory])
                    else:
                        break
                except KeyError as e:
                    df_transitory = pd.DataFrame([[everyRoom,random.randint(0,len(df_item) - 1),random.randint(0,20),everyBranch,snap]],columns=['room','item','amount','branch','snapshot'])
                    df_storage = pd.concat([df_storage,df_transitory])
    
    print('Created Storage')
    return df_storage,df_rooms,df_item

if __name__ == '__main__':
    #Conection with database
    connection = psycopg2.connect(f'dbname=db_logistica user=service_user password={PASSWORD}')
    cursor = connection.cursor()
    
    storage,rooms,itens = makingData()
    
    if not os.path.exists(r'..\DataToInsert'):
        os.mkdir(r'..\DataToInsert')
    
    date = dt.now().strftime('%Y-%m-%d')
    
    #Exporting to Database
    storage.to_csv(os.path.join(r'..\DataToInsert',f'storage_{date}.csv'),sep=';',index=None)
    rooms.to_csv(os.path.join(r'..\DataToInsert',f'rooms_{date}.csv'),sep=';')
    itens.to_csv(os.path.join(r'..\DataToInsert',f'itens_{date}.csv'),sep=';')
    
    cursor.execute('truncate table DIMENSION.DIM_PROD CASCADE')
    cursor.execute('truncate table DIMENSION.DIM_STORAGE_ROOMS CASCADE')
    cursor.execute('truncate table FACT.FT_STORAGE')
    
    cursor.execute(f"COPY DIMENSION.DIM_PROD FROM '{os.path.join(r'C:\Users\Farias\Desktop\PowerBi\DataToInsert',f"itens_{date}.csv")}' (FORMAT 'csv',HEADER,DELIMITER ';' )")    
    cursor.execute(f"COPY DIMENSION.DIM_STORAGE_ROOMS FROM '{os.path.join(r'C:\Users\Farias\Desktop\PowerBi\DataToInsert',f"rooms_{date}.csv")}' (FORMAT 'csv',HEADER,DELIMITER ';' )")
    cursor.execute(f"COPY FACT.FT_STORAGE FROM '{os.path.join(r'C:\Users\Farias\Desktop\PowerBi\DataToInsert',f"storage_{date}.csv")}' (FORMAT 'csv',HEADER,DELIMITER ';' )")
    
    print('export to database completed')
    connection.commit()
    
    
    
    
    
    
    
