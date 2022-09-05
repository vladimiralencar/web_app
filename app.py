# streamlit run app.py 

#pip install -q mysql-connector-python
#pip install -q pymysql
#pip install -q sqlalchemy

import pandas as pd
import numpy as np
import streamlit as st
from sqlalchemy import create_engine

st.title('Mysql Tools - Importar/Exportar')

st.text_input("Database:", key="database", value="aulas")
st.text_input("user:", key="user", value='root')
st.text_input("Password:", key="password", value='rootroot')
st.text_input("Encoding:", key="encoding", value='latin-1')

database = st.session_state.database
user = st.session_state.user
password = st.session_state.password
host = '127.0.0.1' # localhost
port = 3306
schema = database
encoding = st.session_state.encoding
tabela = None

def conecta_banco_de_dados():
    erro = False
    try:
        conexao = "mysql+pymysql://" + user + ":" + password + "@" + host + '/' + schema
        # Abrir a Conexão

        # create SQLAlchemy Engine object instance 
        #engine = sqlalchemy.create_engine(f"{dialect}+{driver}://{login}:{password}@{host}/{database}")

        engine =  create_engine(
                    url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
                    user, password, host, port, database
                )
        )

        #engine = create_engine(conexao, echo = False, pool_recycle=porta)
        return conexao, engine
    except:
        erro = 'erro de conexao'
        st.write(erro)
        return False, False

def consulta_banco_de_dados(cnx, engine, tabela):
    try:
        if cnx is not None and tabela is not None:
            query = "SELECT * from " + tabela +  " limit 100;"
            #result_dataFrame = pd.read_sql(query,cnx)
            #st.write(result_dataFrame)


            # connect to the database using the newly created Engine instance
            connection = engine.connect()
            # run SQL query
            df = pd.read_sql_query(sql=query, con=connection)
            st.write(df)
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
    tabela = None
    st.text_input("tabela:", key="tabela2")
    tabela = st.session_state.tabela2

    # uploaded_file = st.file_uploader("Escolha um arquivo (*.csv)")
    uploaded_file = None
    file = None 

    uploaded_file = st.file_uploader("Escolha um arquivo (*.csv)", key="upload_file")
    file = st.session_state.upload_file

    conexao, engine = False, False
    if file is not None:
        df = pd.read_csv(file, encoding='latin-1') #, encoding='latin-1') #, encoding=result['encoding'])
        st.write(df)
        #st.write("Importar Tabela para o  Mysql")
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
    st.header("Exportar Tabela do Mysql para .CSV")
    tabela3 = None
    st.text_input("tabela:", key="tabela3")

    tabela3 = st.session_state.tabela3

    st.write(tabela3)
    conexao, engine  = conecta_banco_de_dados()
    if conexao is not None and tabela3 is not None:
        query = "SELECT * from " + tabela3 +  " ;"
        #df = pd.read_sql(query,conexao)
        my_connection = engine.connect()
        df = pd.read_sql_query(sql=query, con=my_connection)
        st.write(df)
        df.to_csv(tabela + '.csv', index=False)
        st.write('tabela ' + tabela3 + '.csv' + ' Exportada.')


def consulta_banco_de_dados2(cnx, tabela):
    try:
        if cnx is not None and tabela is not None:
            query = "SELECT * from " + tabela +  " limit 100;"
            result_dataFrame = pd.read_sql(query,cnx)
            st.write(result_dataFrame)


            # connect to the database using the newly created Engine instance
            my_connection = my_engine.connect()

            # run SQL query
            my_df = pd.read_sql_query(sql=my_sql_query, con=my_connection)
    except:
        erro = 'erro de conexao'
