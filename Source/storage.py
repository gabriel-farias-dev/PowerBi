import pandas as pd
import numpy as np
import time
from datetime import datetime as dt, timedelta as td
import logging as log
from faker import Faker
import random



################################################### Making Products in WareHouse
#Variables
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
#storage
for everyRoom,row in df_rooms.iterrows():
    for _ in range(0,900):
        
        try:
            
            if df_storage[df_storage['room'] == everyRoom]['amount'].sum() < row['capacity']:
                df_transitory = pd.DataFrame([[everyRoom,random.randint(0,len(df_item) - 1),random.randint(0,15)]],columns=['room','item','amount'])
                df_storage = pd.concat([df_storage,df_transitory])
            else:
                break
        except KeyError as e:
            df_transitory = pd.DataFrame([[everyRoom,random.randint(0,len(df_item) - 1),random.randint(0,15)]],columns=['room','item','amount'])
            df_storage = pd.concat([df_storage,df_transitory])

print(df_storage)
