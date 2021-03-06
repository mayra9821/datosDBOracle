import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.sql.expression import select,insert


SQL_ALCHEMY_DATABASE_URL = 'oracle://DATOSDECAMPO:paseos@192.168.3.70:1521/sci'
SQL_ALCHEMY_MONITOREO_URL = 'oracle://MONITOREOM:mon2007@192.168.3.70:1521/sci'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)
monitoreo = create_engine(SQL_ALCHEMY_MONITOREO_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base

with monitoreo.connect() as connection2:
    
    query = """ SELECT ID_MUESTREO, ID_PROYECTO
                FROM VM_DATOS_MONITOREO
                WHERE ID_PROYECTO=3002 AND COD_VARIABLE IN ('Pre','RGl','PAT','VA','HR','Ta','DA') """

    queryResult = connection2.execute(query)
    datos = queryResult.fetchall()
    datosDf = pd.DataFrame(datos)
    datosDf.columns = [colName.upper() for colName in queryResult.keys()]

    # agd_muestreos_parametros = pd.DataFrame(columns = ['ID_MUESTREO','ID_PARAMETRO','ID_METODOLOGIA','ID_UNIDAD_MEDIDA','VALOR'])
    inserts = list()
    
    for _, df_muestreo in datosDf.groupby(['ID_MUESTREO']):
        
        insertEntidad = f"""INSERT INTO AGD_MUESTREOS_PARAMETROS (ID_MUESTREO,ID_PARAMETRO,ID_METODOLOGIA,ID_UNIDAD_MEDIDA,VALOR)   
        VALUES ({df_muestreo['ID_MUESTREO'].values[0]},{828},{803},{100},'{'INVEMAR'}')"""
        
        insertProyecto = f"""INSERT INTO AGD_MUESTREOS_PARAMETROS (ID_MUESTREO,ID_PARAMETRO,ID_METODOLOGIA,ID_UNIDAD_MEDIDA,VALOR) 
        VALUES ({df_muestreo['ID_MUESTREO'].values[0]},{127},{803},{100},'{df_muestreo['ID_PROYECTO'].values[0]}')"""
        

        inserts.append(insertEntidad)
        inserts.append(insertProyecto)
    
    
    inserts = pd.DataFrame(data=inserts, columns = ['SQL'])
    print(inserts)
    inserts.to_csv('muestreos_parametros.csv', index=False)
    

with engine.connect() as connection:

    for index, row in inserts.iterrows():
        connection.execute(row['SQL'])
    print('Muestreos agregados')
