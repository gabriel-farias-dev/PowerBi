import pandas as pd
import numpy as np
from datetime import datetime as dt, timedelta
import logging as log

#to make a randomic names, library Faker
from faker import Faker
fake = Faker()

# the datalist to keep the information before a df transformation
datalist = []

#list of dates
dates = [(dt.now() - timedelta(days= td)).strftime('%Y-%m-%d') for td in range(365)]

#routes and branchs 
branchs = ['SP','RJ','DF']
routes = ['001','002','003','004','005','006','007','008','009','010']

#generate fake client names
client = [fake.name() for _ in range(10)]

for everyDate in dates:
    for everyBranch in branchs:
        for everyRoute in routes:
            start_target = ''
            #randomic max hour and min hour
            min_hour =f'{np.random.randint(8,10)}:{np.random.randint(0,60)}:{np.random.randint(0,60)}'
            max_hour =f'{np.random.randint(10,12)}:{np.random.randint(0,60)}:{np.random.randint(0,60)}'
            count_cub = np.random.randint(5,20)

            if everyBranch == 'SP':
                start_target = '08:30:00'

            if everyBranch == 'RJ':
                start_target = '09:00:00'

            if everyBranch == 'DF':
                start_target = '08:45:00'

            min_hour = dt.strptime(min_hour,'%H:%M:%S')
            max_hour = dt.strptime(max_hour,'%H:%M:%S')
            start_target = dt.strptime(start_target,'%H:%M:%S')

            if min_hour > start_target:
                units_before = 0
                units_after = np.random.randint(1,10) * count_cub
            else:
                units_before = np.random.randint(0,100)
                units_after = np.random.randint(0,100)

            total_units = units_before + units_after
            
            datalist.append([everyBranch,everyRoute,everyDate,min_hour,max_hour,count_cub,start_target,units_before,units_after,total_units])

            df = pd.DataFrame(datalist,columns=['branch','route','date','min_hour','max_hour','count_cub','start_target','units_before','units_after','total_units'])

branch = pd.DataFrame([[1,'SP'],[2,'RJ'],[3,'DF']],columns=['id','branch'])