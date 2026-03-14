import pandas as pd
import csv
import numpy as np
from datetime import datetime as dt, timedelta, time, date as datas
import os
import faker as fk
import logging as lg
import random 


#logging configuration and setup of faker

# Primeiro vamos setar algumas filiais que serão usadas, depois pensar nos depositos e rotas
# Todas as filiais devem conter 50 rotas, que as caixas podem sair ou não 
# As rotas são numeros de 3 digitos

# Precisamos agora de clientes, poderia fazer por cd também o que faz mais sentido, já que cada cliente, está em um lugar diferente do pais e deve ser atendido pela branch mais perto, porém não vamos colocar o efeito de localização no dash e todo cliente pode ser atendido por qualquer filial

#Temos clientes, temos rotas, temos filiais, podemos colocar aqui os depositos dos CDs, que são separados por setor

#Lista de listas, que no final vai virar um dataframe
#A tabela final vai conter as seguintes colunas
#CD, DEPOSITO, DATA, CLIENTE,ROTA, CAIXA, UNIDADES, DATA_HORA_SEP, DATA_HORA_CONF, DATA_HORA_EXP, HORA_COMP_SEP, HORA_COMP_CONF,HORA_COMP_EXP,HORA_FORM_EXP,HORA_FORM_CONF,HORA_FORM_EXP
#Percebe que vai conter diversas horas, pelo simples motivo de facilitar as contas que serão feitas dentro do BI, já que as vezes comparamos hora (time) com hora(time), as vezes olhamos somente para a hora mesmo (int)

#Agora preciso pensar em como fazer os horarios, o primeiro horario é o de sep, entre 1 a 10 horas conf, e 1 a 10 horas exp, quero fazer um diferncial para cada cd


lg.basicConfig(filename='shipping.log', level=lg.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
fake = fk.Faker()

branchs = ['SP','RJ','MG','MT','MTS','RS','RN','CE','PR','PB','AL','BA','ES','SC','GO','AC']
routes = {}

for everyBranch in branchs:
    routes[everyBranch] = [random.randint(100,999) for _ in range(50)]

#Dimensões
clients = [[fake.ean(8),fake.company()] for i in range(60)]
departament = ['Eletrodomesticos','Eletronicos','Roupas','Remedios','Comida','Utensilios','Joias','Informatica','Acessorios']
depositos = [[random.randint(0,199), random.choice(departament) ] for _ in range(6)]

#Fato
fato = []

for minusDate in range(-1 * (datas.today() - datas(2026,1,1)).days,0):
    date = (dt.now() + timedelta(days=minusDate)).date()

    for everyBranch in branchs:
        for _ in range(4000):
            ft_departament = random.choice(depositos)[0]
            ft_client = random.choice(clients)[0]

            #times
            minutes = random.randint(0,59)
            seconds = random.randint(0,59)
            hour = random.randint(0,23)
            time_sep = time(hour=hour,minute=minutes,second=seconds)

            date_time_sep = dt.combine(date,time_sep)
            # date.

            minimun = random.randint(1,720)
            maximun = random.randint(minimun,1320)

            minutus_conf = random.randint(minimun,maximun)


            date_time_conf = date_time_sep + timedelta(minutes=minutus_conf)

            minimun = random.randint(1,720)
            maximun = random.randint(minimun,1320)

            minutus_exp = random.randint(minimun,maximun)

            date_time_exp = date_time_sep + timedelta(minutes=minutus_exp)
            
            fato.append([everyBranch,ft_departament, date.__str__(),ft_client,random.choice(routes[everyBranch]),fake.ean13(),random.randint(40,10000),date_time_sep.__str__(),date_time_conf.__str__(),date_time_exp.__str__()])

df_fact = pd.DataFrame(data=fato,columns=['CD', 'DEPOSITO', 'DATA', 'CLIENTE','ROTA', 'CAIXA', 'UNIDADES', 'DATA_HORA_SEP', 'DATA_HORA_CONF', 'DATA_HORA_EXP'])

df_dim_clients = pd.DataFrame(data=clients,columns=['id','name'])
df_dim_departaments = pd.DataFrame(data=depositos,columns=['id','name'])
df_fact = pd.DataFrame(data=fato,columns=['CD', 'DEPOSITO', 'DATA', 'CLIENTE','ROTA', 'CAIXA', 'UNIDADES', 'DATA_HORA_SEP', 'DATA_HORA_CONF', 'DATA_HORA_EXP'])

df_fact.to_csv('../../DataToInsert/shipping.csv',index=None)
df_dim_clients.to_csv('../../DataToInsert/shipping_clients.csv',index=None)
df_dim_departaments.to_csv('../../DataToInsert/shipping_departaments.csv',index=None)