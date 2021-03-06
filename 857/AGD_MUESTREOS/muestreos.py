import pandas as pd
import numpy as np
# import cx_Oracle
from sqlalchemy import create_engine
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.sql.expression import select,insert

# cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_12_2")

SQL_ALCHEMY_DATABASE_URL = 'oracle://DATOSDECAMPO:paseos@192.168.3.70:1521/sci'
SQL_ALCHEMY_MONITOREO_URL = 'oracle://MONITOREOM:mon2007@192.168.3.70:1521/sci'

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)
monitoreo = create_engine(SQL_ALCHEMY_MONITOREO_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base

with monitoreo.connect() as connection2:

    query2 = """SELECT ID_MUESTREO, ID_ESTACION, ID_PROYECTO, FECHA 
    FROM VM_DATOS_MONITOREO 
    WHERE ID_PROYECTO = 1480 AND METODO_ANALITICO = 'Hobos' AND COD_VARIABLE='TEM' and id_muestreo in (12140,12141,12142,12143,12144,12145,12146,12147,
                19681,19682,19683,19687,19693,19694,19752,350514268851590351,
                350514744619290581,350514744631509911,350514744633832571,350514744636127411,350514744638814671,350514744639957221,350514744640744931,
                350514744641603541,350514744642469471,350514744643101901,350514744646894001,350514744647557861,350514744648129961,350514744648958391,
                350514744651166011,350514744656828681,350514744658036711,350514744659322721,350514744660984001,350514744665644491,350514744666258231,
                350514744667728771,350514744668207221,350514744668945601,350514744670292481,350514744680045321,350514744681071191,350514744712450331,
                350514744715772371,350514744717626691,350514744718421491,350514744721746611,350514744732779061,350514744737936451,350514744739355881,
                350514744741022391,350514744741580821,350514744743909311,350514744748047951,350514744748516091,350514744749229411,350514744821502401,
                350514744825601031,350514744848155081,350514744849376391,350514744849926141,350514744861267331,350514744863884681,350514744867098731,
                350514744868778091,350514744871164511,350514744872278161,350514744877043391,350514744878564571,350514744879837431,350514744881579631,
                350514744884247751,350514744885886891,350514744887035741,350514744889541191,350514746378202081,350514746379726461,350514746380495051,
                350514746381156661,350514746382251601,350514746383746571,350514746384306971,350514746384886001,350514746385242911,350514746385979091,
                350514746386364931,350514746386697311,350514746387032031,350514746387368971,350514746387698141,350514746388104011,350514746388519451,
                350514746389107181,350514746389635371,350514746390092851,350514746390384611,350514746390811211,350514746391302371,350514746393026801)"""
    query2Result = connection2.execute(query2)
    datos2 = query2Result.fetchall()
    datos2Df = pd.DataFrame(datos2)
    datos2Df.columns = [colName.upper() for colName in query2Result.keys()]    
    # print(datos2Df['ID_MUESTRA'])
    # agd_muestreos = pd.DataFrame(columns = ['ID_MUESTRA','ID_MUESTREO','NOTAS','ES_REPLICA'])
    muestreos = list()
    # print(datos2Df['ID_MUESTRA'].unique().size)
    for _, df_muestra in datos2Df.groupby('ID_MUESTREO'):
        
        insertMuestreo = f"""INSERT INTO AGD_MUESTREOS (ID_MUESTREO, ID_ESTACION, ID_PROYECTO, ID_METODOLOGIA, ID_TEMATICAS, FECHA)
                        VALUES({str(857)+str(df_muestra['ID_MUESTREO'].values[0])},{df_muestra['ID_ESTACION'].values[0]}, {3492}, {857}, {213}, TO_DATE('{str(df_muestra['FECHA'].values[0]).replace('T',' ').split('.')[0]}','YYYY-MM-DD HH24:MI:SS'))"""
        
        muestreos.append(insertMuestreo)

    muestreos = pd.DataFrame(data=muestreos, columns = ['SQL'])
    print(muestreos)
    # print(pd.DataFrame(datos2Df['ID_MUESTRA']))
    muestreos.to_csv('AGD_MUESTREOS.csv', index=False)

# with engine.connect() as connection:

#     for index, row in muestreos.iterrows():
#         connection.execute(row['SQL'])
#     print('MUESTREOS AGREGADOS')

