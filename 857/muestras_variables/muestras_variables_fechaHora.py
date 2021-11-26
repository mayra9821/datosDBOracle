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

    query2 = """SELECT ID_MUESTREO, ID_CUALIDAD,to_number(substr(to_char((to_number(to_char(to_date(substr(id_cualidad, 1, 8), 'YYYYMMDD'), 'J')) - 2415019 ) + to_number(substr(id_cualidad, 10, 2)) / 24 +
                to_number(substr(id_cualidad, 12, 2)) / ( 60 * 24 ) + to_number(substr(id_cualidad, 14, 2)) / ( 3600 * 24 )),1,21)) AS FECHA
                FROM BMUESTRAS_VARIABLES WHERE ID_MUESTREO IN(350514746639467721,350514746639791561,350514746640084761,350514746640410181,350514746641125821,350514746641965401,
                350514746642310751,350514746642740191,350514746643151051,350514746643585051,350514746644000531,350514746644442351,350514746645002211,
                350514746645576651,350514746646616911,350514746647074621,350514746647440491,350514746647938271,350514746648340221,350514746648714031,
                350514746649037031,350514746649465931,350514746649775531,350514746650201141,350514746650651881,350514746651027681,350514746651257691,
                350514746651643171,350514746651903151,350514746652135781,350514746652436791,350514746652985901,350514746653319891,350514746653538231,
                350514746653876861,350514746654126281,350514746658028331,350514746658519701,350514746659066711,350514746659373371,350514746659799281,
                350514746660095471,350514746660703961,350514746660979411,350514746661352411,350514746661616441,350514746662092401,350514746662438981,
                350514746662730551,350514746663015511,350514746663248761,350514746663532681,350514746664107761,350514746664369051,350514746664929261,
                350514746665272071,350514746665673541,350514746666100651,350514746666440341,350514746666805171,350514746667589901,350514746668129541,
                350514746668596601,350514746668863251,350514746669305791,350514746669691411,350514746670133111,350514746670512541,350514746670791701,
                350514746671294311,350514746671618981,350514746671939341,350514746672304521,350514746672678081,350514746673189081,350514746673484061,
                350514746673961921,350514746674266351,350514746674537061,350514746674856051,350514746675221611,350514746675773361,350514748923577451,
                350514748924201341,350514748924889611,350514748925483901,350514748925966441,350514748926443691,350514748927115381,350514748927561731,
                350514748927977311,350514748928556751,3220201203101317471,3220201203101330511,3220201203101339431,3220201203101351551,3220201203101407541,
                3220201203281708521,3220201203290838041,3220201203290854351,3220201203290909001,3220201203291134571,3220201203291312021,3220201203291421061,
                3220201203291429321,3220201203291454461,3220201204101315051,3220201204101335401,3220201204101346181) """

# 85712000,85712001,85712002,85712003,85712004,85712005,85712006,85712007,85712008,85712009,85712010,85712011,
# 85712012,85712013,85712014,85712015,85712016,85712017,85712018,85712019,85712020,85712021,85712022,85712094,
# 85712096,85712097,85712098,85712099,85712100,85712101,85712102,85712103,85712104,85712105,85712106,85712107
# 85712111,85712112,85712113,85712114,85712115,85712116,85712118,85785719762,85719763,85719764,85712095,
# 85719765,85719766,85719767,85719768,85719769,85719770,85719771,85719772,85719773,85719774,85719775,85719776,85719777,85719778,
# 85719779,85719780,85719781,85719782,85719783,85719784,85719785,85719786,85719787,85719788,85719789,85719790,85719791,85719792,
# 85719793,85719794,85719795,85719796,85719797,85719798,85719799,85719800,85719801,85719802,85719803,85719804,85719805,
# 85719806,85719807,85719808,85712108,85712109,85712110,
    query2Result = connection2.execute(query2)
    datos2 = query2Result.fetchall()
    datos2Df = pd.DataFrame(datos2)
    datos2Df.columns = [colName.upper() for colName in query2Result.keys()]                                                                                                                                          
    datos2Df['COMPLEMENTO'] = datos2Df['ID_CUALIDAD'].apply(lambda x: x.strip().replace(" ","")[0:])
    ##str.extract(r'((?=\s).*)', expand = False).   replace("/","").replace(":","").replace("null","")
    datos2Df['ID_MUESTRA'] = datos2Df['ID_MUESTREO'].astype('str') + datos2Df['COMPLEMENTO'].astype('str')
    # print(datos2Df['ID_MUESTRA'])
    # agd_muestras = pd.DataFrame(columns = ['ID_MUESTRA','ID_MUESTREO','NOTAS','ES_REPLICA'])
    muestras = list()
    # print(datos2Df['ID_MUESTRA'].unique().size)
    for _, df_muestra in datos2Df.groupby('ID_MUESTRA'):
        
        insertFecha = f"""INSERT INTO AGD_MUESTRAS_VARIABLES (ID_PARAMETRO, ID_METODOLOGIA, ID_UNIDAD_MEDIDA, ID_MUESTRA, VALOR)
                        VALUES({646},{857},{100},{df_muestra['ID_MUESTRA'].values[0]}, {df_muestra['FECHA'].values[0]})"""
        
        muestras.append(insertFecha)

    muestras = pd.DataFrame(data=muestras, columns = ['SQL'])                  
    print(muestras)
    # print(pd.DataFrame(datos2Df['ID_MUESTRA']))
    # pd.DataFrame(datos2Df['ID_MUESTRA']).to_csv('muestras.csv', index=False)
    muestras.to_csv('muestras_variables_fechaHora.csv', index=False)

# with engine.connect() as connection:

#     for index, row in muestras.iterrows():
#         connection.execute(row['SQL'])
#     print('MUESTRAS AGREGADAS')    
