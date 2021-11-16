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

with monitoreo.connect() as connection2:
    query2 = """SELECT ID_MUESTREO, ID_CUALIDAD, REPLICA FROM VM_DATOS_MONITOREO WHERE ID_PROYECTO = 1480
                AND ID_MUESTREO IN (447,460,462,454,472,450,466,465,463,457,448,459,475,461,467,471,468,451,455,453,452,469,456,464,470,449)"""

    query2Result = connection2.execute(query2)
    datos2 = query2Result.fetchall()
    datos2Df = pd.DataFrame(datos2)
    datos2Df.columns = [colName.upper() for colName in query2Result.keys()]                                                                                                                                          
    datos2Df['COMPLEMENTO'] = datos2Df['ID_CUALIDAD'].apply(lambda x: x.strip().replace(" ","").replace("/","").replace(":","").replace("null","")[0:])
    ##.str.extract(r'((?=\s).*)', expand = False)
    datos2Df['ID_MUESTRA'] = datos2Df['ID_MUESTREO'].astype('str') + datos2Df['COMPLEMENTO'].astype('str')
    muestras = list()
    ##print(datos2Df['ID_MUESTRA'])
    # agd_muestras = pd.DataFrame(columns = ['ID_MUESTRA','ID_MUESTREO','NOTAS','ES_REPLICA'])
    # print(datos2Df['ID_MUESTRA'].unique().size)
    for _, df_muestra in datos2Df.groupby('ID_MUESTRA'):
        
        insertMuestra = f"""INSERT INTO AGD_MUESTRAS (ID_MUESTRA, ID_MUESTREO,  ES_REPLICA)
                        VALUES({df_muestra['ID_MUESTRA'].values[0]},{str(857)+str(df_muestra['ID_MUESTREO'].values[0])},{df_muestra['REPLICA'].values[0]})"""
        muestras.append(insertMuestra)
    muestras = pd.DataFrame(data=muestras, columns = ['SQL'])                  
    print(muestras)

    # print(pd.DataFrame(datos2Df['ID_MUESTRA']))
    # pd.DataFrame(datos2Df['ID_MUESTRA']).to_csv('muestras.csv', index=False)
    muestras.to_csv('AGD_muestras.csv', index=False)

with engine.connect() as connection:

    for index, row in muestras.iterrows():
        connection.execute(row['SQL'])
    print('MUESTRAS AGREGADAS')