import pandas as pd
import numpy as np
# import cx_Oracle
from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.sql.expression import select,insert
# cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_11_2")


SQL_ALCHEMY_DATABASE_URL = 'oracle://DATOSDECAMPO:paseos@192.168.3.70:1521/sci'
# SQL_ALCHEMY_MONITOREO_URL = 'oracle://MONITOREOM:mon2007@192.168.3.70:1521/sci'
SQL_ALCHEMY_ADMINISTRADOR_URL = 'oracle://administrador:admin*@192.168.3.70:1521/sci'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)
# monitoreo = create_engine(SQL_ALCHEMY_MONITOREO_URL)
administrador = create_engine(SQL_ALCHEMY_ADMINISTRADOR_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base

with administrador.connect() as connection2:

    query = """ SELECT CODIGO_SALIDA, FECHA_MUESTREO
                FROM MCODIGOS_SALIDAS 
                WHERE GRUPO = 'TH'"""
    queryResult = connection2.execute(query)
    datos = queryResult.fetchall()
    datosDf = pd.DataFrame(datos)
    datosDf.columns = [colName.upper() for colName in queryResult.keys()]

    # agd_muestreos_parametros = pd.DataFrame(columns = ['ID_MUESTREO','ID_PARAMETRO','ID_METODOLOGIA','ID_UNIDAD_MEDIDA','VALOR'])
    inserts = list()
    
    for _, df_muestreo in datosDf.groupby(['CODIGO_SALIDA']):
        
        insertEntidad = f"""INSERT INTO AGD_MUESTREOS_PARAMETROS (ID_MUESTREO,ID_PARAMETRO,ID_METODOLOGIA,ID_UNIDAD_MEDIDA,VALOR)   
        VALUES ({str(857)+str(df_muestreo['CODIGO_SALIDA'].values[0])}, {828}, {857}, {100}, '{'INVEMAR'}')"""
        
        insertProyecto = f"""INSERT INTO AGD_MUESTREOS_PARAMETROS (ID_MUESTREO,ID_PARAMETRO,ID_METODOLOGIA,ID_UNIDAD_MEDIDA,VALOR) 
        VALUES ({str(857)+str(df_muestreo['CODIGO_SALIDA'].values[0])},{127},{857},{100},'{1480}')"""
        

        inserts.append(insertEntidad)
        inserts.append(insertProyecto)
    
    
    inserts = pd.DataFrame(data=inserts, columns = ['SQL'])
    print(inserts)
    inserts.to_csv('muestreos_parametros.csv', index=False)
    

# with engine.connect() as connection:

#     for index, row in inserts.iterrows():
#         connection.execute(row['SQL'])
#     print('Muestreos agregados')


