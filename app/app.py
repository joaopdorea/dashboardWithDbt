import os
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
from sqlalchemy import create_engine
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv

import yaml
from yaml.loader import SafeLoader

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
# stauth.Hasher.hash_passwords(config['credentials'])

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)




# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter as variáveis do arquivo .env
DB_HOST = os.getenv('DB_HOST_PROD')
DB_PORT = os.getenv('DB_PORT_PROD')
DB_NAME = os.getenv('DB_NAME_PROD')
DB_USER = os.getenv('DB_USER_PROD')
DB_PASS = os.getenv('DB_PASS_PROD')
DB_SCHEMA = os.getenv('DB_SCHEMA_PROD')

# Criar a URL de conexão do banco de dados
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Criar o engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL)

def get_data():
    query = f"""
    SELECT
        data,
        simbolo,
        valor_fechamento,
        tipo_acao,
        quantidade,
        valor,
        ganho
    FROM
        public.silver_commodities;
    """
    df = pd.read_sql(query, engine)
    return df

def get_receita_liquida():
    query = """
        SELECT SUM(ganho) AS total_ganho
        FROM public.silver_commodities;
    """
    indicador = pd.read_sql(query, engine)
    valor = indicador["total_ganho"].iloc[0]
    return round(valor, 2)

def get_faturamento():
    query = """
        SELECT SUM(ganho) AS faturamento
        FROM public.silver_commodities
        WHERE tipo_acao = 'sell';
    """
    indicador = pd.read_sql(query, engine)
    valor = indicador["faturamento"].iloc[0]
    return round(valor, 2)


def get_despesas():
    query = """
        SELECT SUM(ganho) AS despesa
        FROM public.silver_commodities
        WHERE tipo_acao = 'buy';
    """
    indicador = pd.read_sql(query, engine)
    valor = indicador["despesa"].iloc[0]
    return round(valor, 2)



authenticator.login()


if st.session_state["authentication_status"]:
    authenticator.logout()
    # Configurar a página do Streamlit
    st.set_page_config(page_title='Dashboard do diretor', layout='wide')

    # Título do Dashboard
    st.title('Dashboard commodities')

    # Descrição
    st.write("""
    Este dashboard mostra os dados de commodities e suas transações.
    """)

    # Obter os dados
    df = get_data()

    def format_brl(number):
    # Formata com 2 casas decimais, separador de milhar '.' e decimal ','
        return f"{number:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    receitaLiquida = format_brl(get_receita_liquida())
    faturamento = format_brl(get_faturamento())
    despesa = format_brl(get_despesas())

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
        label="Receita líquida",
        value="R$ "+ str(receitaLiquida)
    )
    
    with col2:
        st.metric(
        label="Faturamento",
        value="R$ "+ str(faturamento)
    )
    
    with col3:
        st.metric(
        label="Despesas",
        value="R$ "+ str(despesa)
    )
    st.dataframe(df)


elif st.session_state["authentication_status"] is False:
    st.error('Usuário/Senha is inválido')
elif st.session_state["authentication_status"] is None:
    st.warning('Por Favor, utilize seu usuário e senha!')

