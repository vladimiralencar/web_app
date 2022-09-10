# streamlit run app.py 

#pip install -q mysql-connector-python
#pip install -q pymysql
#pip install -q sqlalchemy

# pipreqs --force

import pandas as pd
import numpy as np
import streamlit as st
#import sqlalchemy
#from sqlalchemy import create_engine
#import pymysql

st.title('Mysql Tools - Importar/Exportar')

st.text_input("Database:", key="database", value="aulas")
st.text_input("Host:", key="host", value='127.0.0.1')
st.text_input("user:", key="user", value='root')
st.text_input("Password:", key="password", value='rootroot')
st.text_input("Encoding:", key="encoding", value='latin-1')

database = st.session_state.database
user = st.session_state.user
password = st.session_state.password
host = st.session_state.host # "127.0.0.1" # localhost
port = 3306
schema = database
encoding = st.session_state.encoding
tabela = None 

import mysql.connector
# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='rootroot', 
    database='aulas'
    )
    # mydb = mysql.connector.connect(
    # host=host,
    # user=user,
    # password=password, 
    # database=database
    # )

    return mydb

def run_query(conn, query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

# def conecta_banco_de_dados():
#     erro = False
#     try:
#         conexao = "mysql+pymysql://" + user + ":" + password + "@" + host + '/' + schema
 
#         engine =  sqlalchemy.create_engine(
#                     url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
#                     user, password, host, port, database
#                 )
#         )

#         #engine = create_engine(conexao, echo = False, pool_recycle=porta)
#         return conexao, engine
#     except:
#         erro = 'erro de conexao - conecta banco de dados'
#         st.write(erro)
#         return False, False

# def consulta_banco_de_dados(cnx, engine, tabela):
#     try:
#         if cnx is not None and tabela is not None:
#             query = "SELECT * from " + tabela +  " limit 100;"
#             connection = engine.connect()
#             # run SQL query
#             df = pd.read_sql_query(sql=query, con=connection)
#             st.write(df)
#             engine.close()
#     except:
#         erro = 'erro de conexao'

# principal

tab1, tab2, tab3, tab4 = st.tabs(["Visualizar CSV", "Consultar Tabela no MySQL", 
                            "Importar Tabela para MYSQL", "Exportar Tabela do Mysql para .CSV"])

with tab1:
    st.header('Visualizar CSV')
    upload_file_csv = None
    uploaded_file = st.file_uploader("Escolha um arquivo (*.csv)", key="upload_file_csv")
    file = st.session_state.upload_file_csv
    if file is not None:
        df = pd.read_csv(file, encoding=encoding) 
        st.write(df)

with tab2:
    st.header("Consultar Tabela no MySQL")

    st.text_input("tabela:", key="tabela")
    tabela = st.session_state.tabela
    if tabela is not None:

        mycursor = init_connection()
        mycursor.execute("SELECT * FROM " + tabela + ' limit 10')
        myresult = mycursor.fetchall()

        for x in myresult:
            print(x)
    # tabela = None
    # st.text_input("tabela:", key="tabela")
    # tabela = st.session_state.tabela
    # if tabela is not None:
    #     conexao, engine  = conecta_banco_de_dados()
    #     if conexao != False: 
    #         consulta_banco_de_dados(conexao, engine, tabela)

def criar_estrutura_tabela(df, tabela):
    df = df.dtypes.to_frame().reset_index()
    df.columns = ['atributo', 'tipo']
    df3 = df.copy()
    df4 = df.copy()
    df4['tipo'] = df3['tipo'].apply(lambda x: str(x))
    df4['tipo'] = df4['tipo'].apply(lambda x: 'text' if x == 'object'  else x)
    df4['tipo'] = df4['tipo'].apply(lambda x: 'text' if x == 'bool' else x)
    df4['tipo'] = df4['tipo'].apply(lambda x: 'float' if x == 'float64' else x)
    df4['tipo'] = df4['tipo'].apply(lambda x: 'bigint' if x == 'int64' else x)

    sql_create_table = "create table "+ tabela + "(\n"
    for index, row in df4.iterrows():
        #print(row['atributo'] + "\t" + str(row['tipo']))
        sql_create_table = sql_create_table + '`' + row['atributo'] +  '`' + \
                                             "\t" + str(row['tipo']) + ',\n'
    sql_create_table = sql_create_table[:-2] +  "\n);"
    return sql_create_table

def criar_estrutura_inserir_tabela(df, tabela):
    num_atributos = len(df.columns)
    formato = '%s, ' * num_atributos 
    formato = formato[:-2]
    sql_insert_table = "INSERT INTO "+ tabela + " VALUES (" + formato + ")\n" 
    sql_values = []
    for index, row in df.iterrows():
        sql_values.append( tuple(row) )
    #print(sql_insert_table)
    #print(sql_values)  

    return sql_insert_table, sql_values

with tab3:
    st.header("Importar Tabela para MYSQL")
    tabela2 = None
    st.text_input("tabela MySQL:", key="tabela2")
    

    tabela = st.session_state.tabela2


    uploaded_file = None
    file = None 

    uploaded_file = st.file_uploader("Escolha um arquivo (*.csv)", key="upload_file")
    file = st.session_state.upload_file

    #df = pd.read_csv(file)
    #atributos = df.columns.values
    #conn = init_connection()
    
    conexao, engine = False, False
    if file is not None:
        df = pd.read_csv(file, encoding='latin-1') 
        st.write(df)
        #conexao, engine = conecta_banco_de_dados()

        mydb = conn = conexao = init_connection()

        if tabela is not None:
            if conexao != False: 
                st.write('importando no MySQL...')
                # dataframe => como tabela no MySQL
                #df.to_sql(name = tabela, con = engine, if_exists = 'append', index = False)
                
                estrutura_tabela_SQL = criar_estrutura_tabela(df, tabela)
                estrutura_ok = run_query(conn, estrutura_tabela_SQL) 

                sql_insert, values = criar_estrutura_inserir_tabela(df, tabela)

                mycursor = mydb.cursor()
                # sql = "INSERT INTO customers VALUES (%s, %s)"
                # val = [
                #   ('Peter', 'Lowstreet 4'),
                #   ('Amy', 'Apple st 652'),
                #   ('Hannah', 'Mountain 21'),
                #   ('Michael', 'Valley 345'),
                #   ('Sandy', 'Ocean blvd 2'),
                #   ('Betty', 'Green Grass 1'),
                #   ('Richard', 'Sky st 331'),
                #   ('Susan', 'One way 98'),
                #   ('Vicky', 'Yellow Garden 2'),
                #   ('Ben', 'Park Lane 38'),
                #   ('William', 'Central st 954'),
                #   ('Chuck', 'Main Road 989'),
                #   ('Viola', 'Sideway 1633')
                # ]

                mycursor.executemany(sql_insert, values)

                mydb.commit()


                #rows = run_query(conn, "INSERT * FROM " + tabela + ";") 
                st.write('importado no MySQL.')
                #st.write(df)
            else:
                st.write('Erro de conexão tab3')



with tab4:
    tabela = None
    st.header("Exportar Tabela do Mysql para .CSV")
    tabela3 = None
    st.text_input("tabela:", key="tabela3")
    tabela = st.session_state.tabela3

    arquivo_destino = None
    st.text_input("Nome do arquivo destino:", key="arquivo", 
        value='/home/valencar/Documents/arquivo.csv')
    arquivo_destino = st.session_state.arquivo    


    st.write(tabela)


    # conexao, engine  = conecta_banco_de_dados()
    # if conexao is not None and tabela is not None \
    #             and arquivo_destino is not None:
    #     query = "SELECT * from " + tabela +  " ;"
    #     #df = pd.read_sql(query,conexao)
    #     try:
    #         st.write('exportando...')
    #         connection = engine.connect()
    #         df = pd.read_sql_query(sql=query, con=connection)
    #         st.write(df)
    #         df.to_csv(arquivo_destino, index=False)
    #         st.write('tabela ' + arquivo_destino + '.csv' + ' Exportada.')
    #         engine.close()
    #         st.write('Arquivo exportado...')
    #     except:
    #         st.write('erro de conexao tab 4')
    # else: 
    #     st.write('none') 

