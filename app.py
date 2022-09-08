# streamlit run app.py 

#pip install -q mysql-connector-python
#pip install -q pymysql
#pip install -q sqlalchemy

# pipreqs --force

import pandas as pd
import numpy as np
import streamlit as st
import sqlalchemy
#from sqlalchemy import create_engine
import pymysql

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

def conecta_banco_de_dados():
    erro = False
    try:
        conexao = "mysql+pymysql://" + user + ":" + password + "@" + host + '/' + schema
 
        engine =  sqlalchemy.create_engine(
                    url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
                    user, password, host, port, database
                )
        )

        #engine = create_engine(conexao, echo = False, pool_recycle=porta)
        return conexao, engine
    except:
        erro = 'erro de conexao - conecta banco de dados'
        st.write(erro)
        return False, False

def consulta_banco_de_dados(cnx, engine, tabela):
    try:
        if cnx is not None and tabela is not None:
            query = "SELECT * from " + tabela +  " limit 100;"
            connection = engine.connect()
            # run SQL query
            df = pd.read_sql_query(sql=query, con=connection)
            st.write(df)
            engine.close()
    except:
        erro = 'erro de conexao'

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
    tabela = None
    st.text_input("tabela:", key="tabela")
    tabela = st.session_state.tabela
    if tabela is not None:
        conexao, engine  = conecta_banco_de_dados()
        if conexao != False: 
            consulta_banco_de_dados(conexao, engine, tabela)

with tab3:
    st.header("Importar Tabela para MYSQL")
    tabela2 = None
    st.text_input("tabela MySQL:", key="tabela2")
    

    tabela = st.session_state.tabela2


    uploaded_file = None
    file = None 

    uploaded_file = st.file_uploader("Escolha um arquivo (*.csv)", key="upload_file")
    file = st.session_state.upload_file

    conexao, engine = False, False
    if file is not None:
        df = pd.read_csv(file, encoding='latin-1') 
        st.write(df)
        conexao, engine = conecta_banco_de_dados()

        if tabela is not None:
            if conexao != False: 
                # dataframe => como tabela no MySQL
                df.to_sql(name = tabela, con = engine, if_exists = 'append', index = False)
                st.write('importado no MySQL.')
                #st.write(df)
        else: 
            st.write('digite o nome da tabela')

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
    conexao, engine  = conecta_banco_de_dados()
    if conexao is not None and tabela is not None \
                and arquivo_destino is not None:
        query = "SELECT * from " + tabela +  " ;"
        #df = pd.read_sql(query,conexao)
        try:
            df.write('exportando...')
            connection = engine.connect()
            df = pd.read_sql_query(sql=query, con=connection)
            st.write(df)
            df.to_csv(arquivo_destino, index=False)
            st.write('tabela ' + arquivo_destino + '.csv' + ' Exportada.')
            engine.close()
            df.write('Arquivo exportado...')
        except:
            print('erro de conexao tab 4')
    else: 
        st.write('none') 

