import streamlit as st
import pandas as pd
import plotly.express as px
import os

PATH = os.path.join(os.getcwd(),'excel')
def generate_list():
    if not os.path.exists(PATH):
        os.mkdir('excel')
    return os.listdir(PATH)


f = st.sidebar.file_uploader(label='Arquivo',label_visibility='visible')
if f:
    fb = open(f'./excel/{f.name}.xlsx','wb')
    fb.write(f.getvalue())
    fb.close()
    turmas = pd.DataFrame({'turma':os.listdir(PATH)})

if generate_list():
    turmas = pd.DataFrame({'turma':generate_list()})        
    #unique person

    turma_name = st.sidebar.selectbox('Turma',turmas['turma'].unique())
    geral = st.button(label='Analise da Turma', type='primary',use_container_width=True,help='Informações gerais sobre uma turma')
    turma = pd.read_excel(os.path.join(PATH,turma_name)).filter(items=['Name','Total Marks','Rank','Correct Answers','AVALIAÇÃO DIAGNÓSTICA -Língua Portuguesa ','Incorrect Answers','Q 1 Marks','Q 1 Pontos','Q 2 Marks','Q 3 Marks','Q 4 Marks','Q 5 Marks','Q 6 Marks','Q 7 Marks','Q 8 Marks','Q 9 Marks','Q 10 Marks'])
    name = st.sidebar.selectbox('Alunos', turma['Name'].unique())

    if geral:
        container = st.container(border=False)
        container.title(body=turma_name)
        rank_alunos = turma.filter(items=['Name','Correct Answers'])
        container.plotly_chart(px.bar(data_frame=rank_alunos,y=rank_alunos['Correct Answers'],x=rank_alunos['Name'],color=rank_alunos['Name'],title='Notas dos alunos',range_y=(0,20),width=200),use_container_width=True)
    elif turma_name:
        container = st.container(border=False)

        dt_filter_aluno = turma[turma['Name'] == name]
        container.title(name)
        c10, c11 = container.columns(2,gap='large')
        aluno = dt_filter_aluno.filter(items=['Total Marks','Rank','AVALIAÇÃO DIAGNÓSTICA -Língua Portuguesa ']).melt(var_name='ASSUNTO',value_name='VALOR')
        aluno['ASSUNTO'][2] = 'Nº Port / Math'
        aluno['VALOR'][2] = f'{aluno['VALOR'][2]} / {aluno['VALOR'].get(0) - aluno['VALOR'].get(2)}'
        pontos = dt_filter_aluno.melt(var_name='ASSUNTO',value_name='VALOR').drop(range(6))
        cor_inc = dt_filter_aluno.filter(items=['Correct Answers','Incorrect Answers'])

        c10.write('INFORMAÇÕES')
        c10.dataframe(aluno,hide_index=True,use_container_width=True)
        c10.dataframe(cor_inc,hide_index=True,use_container_width=True)

        c11.write('NOTAS')
        c11.dataframe(data=pontos,hide_index=True,use_container_width=True)
