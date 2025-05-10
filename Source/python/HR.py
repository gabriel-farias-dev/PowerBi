#Importando as bibliotecas que vou usar
import pandas as pd
import numpy
from faker import Faker
from datetime import datetime as dt,timedelta
import psycopg2
import logging as log
import random
from secrets_psql import HOST,PASSWORD
import os

def create_base_hr() -> pd.DataFrame:
    """Para esse BI, vou usar as seguintes colunas para fazer uma analise de Absenteismo e Horas Extras
     - Matricula
     - Colaborador
     - filial
     - GestorDireto
     - Derpartamento
     - Expediente
     - Data
     - Horas previstas
     - Horas trabalhadas
     - Falta
     - Motivo falta
     
     Pra isso preciso setar primeiro as seguintes listas: filial,gestor,departamento,
     expediente,motivo da falta
    """
    fake = Faker()
    final_data = []

    #Branchs - Filiais
    branch_names = ['Blue', 'Yellow', 'Red', 'DeepBlue', 'Green', 'Purple', 'Pink', 'Orange', 'Brown', 'White', 'Black', 'Gray', 'Magenta', 'Cyan']

    #Departamentos
    Departament = ['Logistica','TI','Manutenção','RH','Planejamento Financeiro','Planejamento Logistico']

    #Managers - Nomes Gestor
    manager = [fake.name() for _ in range(70)]

    #Office Hours - Expediente
    office_hours = ['08:00 - 17:00','14:00 - 23:00','23:00 - 08:00']

    #absence reason - falta
    absence_reason = ['Férias','Atestado','Afastamento','Falta','Assinuidade','Convocação Judicial','Falencimento Familiar']

    #Agora preciso linkar as filiais com os gestores, cada filial precisa ter 5 gestores
    #Embaralhando os gestores e criando um dicionario
    random.shuffle(manager)
    branch_manager = {}

    #For para cada filial receber um gestor
    for i,branch in enumerate(branch_names):
        j = i * 5
        branch_manager[branch] = manager[j:j+5]
       
    #Agora podemos começar a fazer as pessoas que serão analisadas, dando todas as informações delas
    temp = []
    for everyKey in branch_manager.keys():
        print(f'Branch: {everyKey}')
        for everyManager in branch_manager[everyKey]:
            
            for _ in range(15):
                ofhr = random.choice(office_hours)
                depar = random.choice(Departament)
                nome = fake.name()
                matricula = fake.unique.random_int(min=100000,max=999999)
                for i in range(397):
                    date = (dt.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                    #se for true quer dizer que faltou
                    if random.choices([True, False], weights=[10, 90])[0]:     
                        rea = random.choice(absence_reason)
                        temp = [matricula,nome,everyKey,everyManager,depar,ofhr,date,540,0,True,rea]
                        final_data.append(temp)
                    else:
                        temp = [matricula,nome,everyKey,everyManager,depar,ofhr,date,540,fake.random_int(min=430, max=700),False,'']
                        final_data.append(temp)

    df = pd.DataFrame(final_data,columns = ['Matricula','nome','branch','Manager','departamento','expediente','data','horas_previstas','horas_trabalhadas','Falta','Motivo_falta'])
    
    return df
    
if __name__ == '__main__':
    #Conection with database
    connection = psycopg2.connect(f'dbname=db_logistica user=service_user password=')
    cursor = connection.cursor()
    
    #Caso não exista a pasta onde vai ficar o arquivo consolidado
    if not os.path.exists(r'..\DataToInsert'):
        os.mkdir(r'..\DataToInsert')
        
    date = dt.now().strftime('%Y-%m-%d')
    
    df = create_base_hr()
    df.to_csv(os.path.join(r'..\DataToInsert',f'hr_{date}.csv'),index=None,sep=';')
    
    #Inserindo
    cursor.execute('truncate table fact.ft_hr')
    cursor.execute(f"COPY FACT.FT_HR FROM '{os.path.join(r'C:\Users\Farias\Desktop\PowerBi\DataToInsert',f'hr_{date}.csv')}' (FORMAT 'csv',header,delimiter ';')");
    connection.commit()
    print('inserindo com sucesso')
    
    







