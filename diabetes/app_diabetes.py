import pickle 
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import sklearn 

# git lfs migrate import --include="*.pck"


# pipreqs

st.title('Sistema para Previsão de Diabetes')
st.sidebar.title("Atributos")

# # variaveis 
atributos = ['Diagnostico_Diabetes', 'Pressao_Alta', 'Colesterol_Alto', 'Checagem_Colesterol_em_5_anos', 'IMC', 'Fumante', 'AVC', 'Doenca_coronaria_cardiaca', 'Atividade_Fisica_nos_ultimos_30_dias', 'Consumo_Frutas', 'Consumo_Vegetais', 'Alto_Consumo_Alcool', 'Plano_de_Saude', 'Nao_pode_ir_ao_medico_devido_custo', 'Estado_Geral_Saude', 'Saude_mental', 'Saude_fisica', 'Dificuldade_andar_ou_subir_escadas', 'Sexo', 'Idade', 'Nivel_Educacional', 'Renda']

 # inicializacao das variaveis
Diagnostico_Diabetes= Pressao_Alta= Colesterol_Alto= Checagem_Colesterol_em_5_anos= IMC= Fumante= AVC= Doenca_coronaria_cardiaca= Atividade_Fisica_nos_ultimos_30_dias= Consumo_Frutas= Consumo_Vegetais= Alto_Consumo_Alcool= Plano_de_Saude= Nao_pode_ir_ao_medico_devido_custo= Estado_Geral_Saude= Saude_mental= Saude_fisica= Dificuldade_andar_ou_subir_escadas= Sexo= Idade= Nivel_Educacional= Renda =  0 

with st.sidebar:

    with st.form(key='my_form'):

        def format_func(option):
            return CHOICES[option]
    

        CHOICES = {0: "Não", 2: "Sim"}
        Pressao_Alta  = st.selectbox('Pressão Alta', options=list(CHOICES.keys()), format_func=format_func)
        Colesterol_Alto = st.selectbox('Colesterol Alto',options=list(CHOICES.keys()), format_func=format_func)
        Checagem_Colesterol_em_5_anos  = st.selectbox(
            'Checagem colesterol em 5 anos',options=list(CHOICES.keys()), format_func=format_func)

        IMC = st.number_input('IMC', min_value=25.0, max_value=500.0, step=1.0)

        Fumante = st.selectbox('Fumante',options=list(CHOICES.keys()), format_func=format_func)

        AVC = st.selectbox('AVC',options=list(CHOICES.keys()), format_func=format_func)

        CHOICES = {0: "Não", 2: "Sim"}
        Doenca_coronaria_cardiaca  = st.selectbox('Doenca coronária cardíaca',
                                                    options=list(CHOICES.keys()), format_func=format_func)

        CHOICES = {0: "Não", 2: "Sim"}
        # physical activity in past 30 days - not including job 0 = no 1 = yes
        Atividade_Fisica_nos_ultimos_30_dias = st.selectbox(
            'Atividade Física nos últimos 30 dias',
            options=list(CHOICES.keys()), format_func=format_func)


        CHOICES = {0: "Não", 2: "Sim"}
        Consumo_Frutas  = st.selectbox('Consumo de Frutas',options=list(CHOICES.keys()), format_func=format_func)

        Consumo_Vegetais = st.selectbox('Consumo de Vegetais',options=list(CHOICES.keys()), format_func=format_func)

        Alto_Consumo_Alcool = st.selectbox('Alto Consumo de Alcool',options=list(CHOICES.keys()), format_func=format_func)

        Plano_de_Saude = st.selectbox('Plano de Saúde',options=list(CHOICES.keys()), format_func=format_func)

        Nao_pode_ir_ao_medico_devido_custo  = st.selectbox(
            'Não pode ir ao medico devido ao custo',options=list(CHOICES.keys()), format_func=format_func)
        
        # 1 = excellent 2 = very good 3 = good 4 = fair 5 = poor
        CHOICES = {1: "Excelente" , 2: "Muito Bom", 3: "Bom", 4: "Razoável", 5: "Ruim"}
        Estado_Geral_Saude = st.selectbox('Estado Geral de Saúde',
            options=list(CHOICES.keys()), format_func=format_func)

        Saude_mental  = st.number_input('Problemas com Saude Mental (em dias)',
                                min_value=0, max_value=30)

        Saude_fisica = st.number_input('Problemas com Saude Física (em dias)',
                                min_value=0, max_value=30)

        Dificuldade_andar_ou_subir_escadas = st.selectbox(
            'Dificuldade de andar ou subir escadas',options=list(CHOICES.keys()), format_func=format_func)

        CHOICES = {0: "Maculino", 1: "Feminino"}
        Sexo = st.selectbox('Sexo',options=list(CHOICES.keys()), format_func=format_func)

        CHOICES = {1: "18-24", 2: "25-29", 3: "30-34", 4: "35-39", 5: "40-44", 6: "45-49", 7: "50-54",
                    8: "55-59", 9: "60-64", 10: "65-69", 11: "70-74", 12: "75-79", 13:"80+"}
        Idade  = st.selectbox('Idade', options=list(CHOICES.keys()), format_func=format_func)

        #1 = Never attended school or only kindergarten 2 = Grades 1 through 8 (Elementary) 3 = Grades 9 through 11 (Some high school) 4 = Grade 12 or GED (High school graduate) 5 = College 1 year to 3 years (Some college or technical school) 6 = College 4 years or more (College graduate)
        CHOICES = {1: 'Não frequentou a escola', 2: 'Ensino Básico', 3: 'Ensino Médio Incompleto', 
                   4: 'Ensino Médio Completo', 4: "Faculdade (1 a 3 anos) ou Técnico", 
                   5: "Superior Completo" }
        Nivel_Educacional  = st.selectbox('Nivel Educacional',
            options=list(CHOICES.keys()), format_func=format_func)

        CHOICES = { 1:'Menos de $10,000', 2:'$10,000 até menos que $15,000', 
                    3:'$15,000 até menos que $20,000', 4:'$20,000 até menos que $25,000',
                    5:'$25,000 até menos que $35,000', 6:'$35,000 até menos que $50,000',
                    8:'$50,000 até menos que $75,000', 9:'Mais de $75,00' }

        Renda = st.selectbox('Renda Anual (em Dólar)',
            options=list(CHOICES.keys()), format_func=format_func)

        predict_button = st.form_submit_button(label='Prever')


# Pagina pricipal

def previsao_diabetes(Pressao_Alta, Colesterol_Alto, Checagem_Colesterol_em_5_anos, IMC, Fumante, AVC, 
                      Doenca_coronaria_cardiaca, Atividade_Fisica_nos_ultimos_30_dias, 
                      Consumo_Frutas, Consumo_Vegetais, Alto_Consumo_Alcool, 
                      Plano_de_Saude, Nao_pode_ir_ao_medico_devido_custo, Estado_Geral_Saude, 
                      Saude_mental, Saude_fisica, Dificuldade_andar_ou_subir_escadas, Sexo, 
                      Idade, Nivel_Educacional, Renda):
        # 0 = no diabetes 1 = prediabetes 2 = diabetes

    new_X = np.array([Pressao_Alta, Colesterol_Alto, Checagem_Colesterol_em_5_anos, IMC, Fumante, AVC, 
                      Doenca_coronaria_cardiaca, Atividade_Fisica_nos_ultimos_30_dias, 
                      Consumo_Frutas, Consumo_Vegetais, Alto_Consumo_Alcool, 
                      Plano_de_Saude, Nao_pode_ir_ao_medico_devido_custo, Estado_Geral_Saude, 
                      Saude_mental, Saude_fisica, Dificuldade_andar_ou_subir_escadas, Sexo, 
                      Idade, Nivel_Educacional, Renda])

    #file = "modelo_rf.pkl" 
    #xgb = joblib.load(file)

    rf = pickle.load(open('diabetes/modelo_rf.pkl', 'rb')) 

    # with open('modelo_rf.pkl', 'rb') as f:
    #     rf = cPickle.load(f)

    preds = rf.predict(new_X.reshape(1, -1) )[0]
    #preds

    # st.write(Pressao_Alta, Colesterol_Alto, Checagem_Colesterol_em_5_anos, IMC, Fumante, AVC, 
    #                   Doenca_coronaria_cardiaca, Atividade_Fisica_nos_ultimos_30_dias, 
    #                   Consumo_Frutas, Consumo_Vegetais, Alto_Consumo_Alcool, 
    #                   Plano_de_Saude, Nao_pode_ir_ao_medico_devido_custo, Estado_Geral_Saude, 
    #                   Saude_mental, Saude_fisica, Dificuldade_andar_ou_subir_escadas, Sexo, 
    #                   Idade, Nivel_Educacional, Renda)
    
    diagnostico_previsto = preds

    if diagnostico_previsto == 0:
        Diagnostico_Diabetes = "Sem Diabetes"
        image = 'saudavel.jpg' 
    elif diagnostico_previsto == 1:
        Diagnostico_Diabetes = "Diabetes"
        image = 'diabetes02.jpg' 
    else:
        Diagnostico_Diabetes = "Sem Diagnóstico"

    return Diagnostico_Diabetes, image


if predict_button:
    Diagnostico_Diabetes, imagem  = previsao_diabetes(Pressao_Alta, Colesterol_Alto, 
                                              Checagem_Colesterol_em_5_anos, IMC, Fumante, AVC, 
                                              Doenca_coronaria_cardiaca, Atividade_Fisica_nos_ultimos_30_dias, 
                                              Consumo_Frutas, Consumo_Vegetais, Alto_Consumo_Alcool, 
                                              Plano_de_Saude, Nao_pode_ir_ao_medico_devido_custo, Estado_Geral_Saude, 
                                              Saude_mental, Saude_fisica, Dificuldade_andar_ou_subir_escadas, Sexo, 
                                              Idade, Nivel_Educacional, Renda)
    

    #st.write(Diagnostico_Diabetes)
    image = Image.open('diabetes/' + imagem)
    st.markdown('## Diagnóstico: ' + '__' + Diagnostico_Diabetes + '__')
    #st.write('Diagnóstico:' + Diagnostico_Diabetes)
    st.image(image, width=250)

else:
    Diagnostico_Diabetes = 'Sem Previsão' 

