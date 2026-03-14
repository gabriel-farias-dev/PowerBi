import logging
import psycopg2
from datetime import datetime as dt,timedelta
import pandas as pd
import numpy as np
import random
from faker import Faker

#Primeiro vamos inciar o Faker, iniciar as branchs, fazer os cdgs dos itens e fazer cdg de clientes 
fake = Faker('pt-BR')
branchs = ['SP','MG','PA','PR']
codeItens = [fake.random_int(100000,999999) for i in range(10000)]
codeClients = [fake.random_int(1000,9999) for i in range(2000)]

#Cada requisição de compra vai precisar de um tipo
typeRequest = ['Success','Cancelled']

#dicionario onde vai as informaçoes dos horarios das branchs, e numero maximo de pedidos 
branchDict = {}


#Vamos para algumas premissas das requisicoes de compras.
# 1: Vai existir data de pedido,data da remessa, data de cubagem, data de Conferencia, data de expedição (todos com horario)
# 2: Vamos ter também um status de um sistema de retardamento de pedido, que vamos chamar de DelaySystem
# 3: Vamos pensar também nos horarios que devem sair mais pedidos, e para isso vamos criar uma função que vai gerar mais pedidos em determinados horarios
# 4: Precisamos que seja bem condizente com a realidade,e para isso vamos usar bastante probalidades
# Entenda que vamos ter q criar varios loops , passando por branch e por dia, talvez demore um pouco a funcionalidade

def probabilityHours() -> dict:
    hoursPeak = {}
    growthRate = random.randint(10,40) / 100
    declineRate = random.randint(10,40) / 100

    #Irei retornar um dicionario que a chave vai ser o horario + probabilidade de gerar pedidos
    for i in range(8,20):

        if i == 8: 
            hoursPeak[i] = growthRate
            continue
        
        if max(hoursPeak.values()) < 0.95:
            hoursPeak[i] = hoursPeak[i - 1] + growthRate
        else:
            hoursPeak[i] = hoursPeak[i - 1] - declineRate if hoursPeak[i - 1] - declineRate > 0 else 0

    return hoursPeak

def logisticHours(hourReq,status,day) -> dict:

    dayOfShip = dt.now() - timedelta(day)
    dayOfShip.replace(hour = hourReq)
    dayOfShip.replace(minute = random.randint(0,59))

    if status == 'Cancelled':
        hoursCancelled = random.randint(0,10)
        dayOfCancelled = dayOfShip + timedelta(hours=hoursCancelled)
        
        return {
        'dayOfCancelled': dayOfCancelled,
        'dayOfShipment': None,
        'dayOfCubing': None,
        'dayOfConf': None,
        'dayOfDispatch':None
        }
    
    hoursShipment = hourReq + 1
    hoursCubing = hoursShipment + random.randint(0,10)
    hoursConf = hoursCubing + 1
    hoursDispatch  = hoursConf + 1

    dayOfShipment = dayOfShip + timedelta(hours=hoursShipment)
    dayOfCubing = dayOfShip + timedelta(hours=hoursCubing)
    dayOfConf = dayOfShip + timedelta(hours=hoursConf)
    dayOfDispatch = dayOfShip + timedelta(hours=hoursDispatch)

    return {
        'dayOfCancelled': None,
        'dayOfShipment': dayOfShipment,
        'dayOfCubing': dayOfCubing,
        'dayOfConf': dayOfConf,
        'dayOfDispatch':dayOfDispatch
    }

for branch in branchs:
    branchDict[branch] = {
        'Hours': probabilityHours(),
        'MaxReq': random.randint(100,1000)
    }

#Vamos gerar os pedidos por branch

pedido = []
#loop branch
for branch in branchs:
    print(f'Branch: {branch}')

    #loop dia
    for everyDay in range(-360,0):
        dateNow = (dt.now() - timedelta(days=everyDay)).strftime('%Y-%m-%d')
        
        # loop por hora
        for everyHour in range(8,20):

            #loop por pedido
            for everyReq in range(0,int(branchDict[branch]['MaxReq'] * branchDict[branch]['Hours'][everyHour])):
                status = random.choice(typeRequest)
                timeReq = ((dt.now() - timedelta(days=everyDay)).replace(minute = random.randint(0,59))).strftime('%H:%M:%S')

                #Para descontruir os horarios que vem da função., preciso primeiro deixar como tupla os valores, então vamos fazer uma jogada
                result = logisticHours(hourReq=everyHour,status= status, day=everyDay)
                dayOfCancelled,dayOfShipment,dayOfCubing,dayOfConf,dayOfDispatch = (
                    result['dayOfCancelled'],
                    result['dayOfShipment'],
                    result['dayOfCubing'],
                    result['dayOfConf'],
                    result['dayOfDispatch']
                    
                )
                units = random.randint(1,100)
                item = random.choice(codeItens) 

                pedido.append([str(random.randint(10000000,99999999)),branch,dateNow,timeReq,status,item,units,dayOfCancelled,dayOfShipment,dayOfCubing,dayOfConf,dayOfDispatch])

df = pd.DataFrame(pedido,columns=['NR_PEDIDO','BRANCH','DATA_ORDEM_VENDA','HORA_ORDEM_VENDA','STATUS','MATERIAL','UNIDADES','DATA_CANCELAMENTO','DATA_REMESSA','DATA_CUBAGEM','DATA_CONF','DATA_EXPEDICAO'])

print(df)



    
    

        
    

