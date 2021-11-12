import pandas as pd
import numpy as np
import cx_Oracle
from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.sql.expression import select,insert
cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_11_2")


SQL_ALCHEMY_DATABASE_URL = 'oracle://DATOSDECAMPO:paseos@192.168.3.70:1521/sci'
SQL_ALCHEMY_MONITOREO_URL = 'oracle://MONITOREOM:mon2007@192.168.3.70:1521/sci'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)
monitoreo = create_engine(SQL_ALCHEMY_MONITOREO_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base

with engine.connect() as connection2:

    query2 = """SELECT ID_MUESTREO, ID_ESTACION, ID_PROYECTO, FECHA, NOTAS_GENERALES
                FROM VM_AGM_2507_816 
                WHERE VARIABLE IN ('140','141','142','143','483','484','482') and PROYECTO is NULL AND FECHA_HORA LIKE ('%/2018%')"""

    query2Result = connection2.execute(query2)
    datos2 = query2Result.fetchall()
    datos2Df = pd.DataFrame(datos2)
    datos2Df.columns = [colName.upper() for colName in query2Result.keys()]    
    # print(datos2Df['ID_MUESTRA'])
    # agd_muestras = pd.DataFrame(columns = ['ID_MUESTRA','ID_MUESTREO','NOTAS','ES_REPLICA'])
    muestras = list()
    # print(datos2Df['ID_MUESTRA'].unique().size)
    for _, df_muestra in datos2Df.groupby('ID_MUESTREO'):
        
        insertMuestreo = f"""INSERT INTO AGD_MUESTREOS (ID_MUESTREO, ID_ESTACION, ID_PROYECTO, ID_METODOLOGIA, ID_TEMATICAS, FECHA) 
        VALUES({str(803)+str(df_muestra['ID_MUESTREO'].values[0])},{df_muestra['ID_ESTACION'].values[0]}, {2507}, {803}, {213}, TO_DATE('{str(df_muestra['FECHA'].values[0]).replace('T',' ').split('.')[0]}','YYYY-MM-DD HH24:MI:SS'))"""
        
        muestras.append(insertMuestreo)

    muestras = pd.DataFrame(data=muestras, columns = ['SQL'])                  
    print(muestras)
    # print(pd.DataFrame(datos2Df['ID_MUESTRA']))
    # pd.DataFrame(datos2Df['ID_MUESTRA']).to_csv('muestras.csv', index=False)
    muestras.to_csv('AGD_MUESTREOS.csv', index=False)

with engine.connect() as connection:

    for index, row in muestras.iterrows():
        connection.execute(row['SQL'])
    print('MUESTREOS AGREGADOS')





