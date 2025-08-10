# 📊 Pipeline de Coleta e Armazenamento de Commodities

Este projeto coleta dados de preços de commodities utilizando a biblioteca [yfinance](https://pypi.org/project/yfinance/), organiza-os em um DataFrame com o [pandas](https://pandas.pydata.org/) e armazena as informações em um banco de dados PostgreSQL utilizando [SQLAlchemy](https://www.sqlalchemy.org/).

## 🚀 Funcionalidades
- Busca preços de commodities (petróleo, ouro e prata) via API do Yahoo Finance
- Armazena os dados no PostgreSQL
- Código modular com funções reutilizáveis

## 📦 Bibliotecas utilizadas
- `yfinance`
- `pandas`
- `sqlalchemy`
- `python-dotenv`
- `os`

## 📂 Estrutura do Fluxo

```mermaid
flowchart TD
    A[Inicio] --> B[Carregar bibliotecas: yfinance, pandas, sqlalchemy, dotenv, os]
    B --> C[Carregar variaveis de ambiente .env]
    C --> D[Definir lista de commodities: CL=F, GC=F, SI=F]
    D --> E[Obter credenciais do banco de dados a partir das variaveis de ambiente]
    E --> F[Montar DATABASE_URL]
    F --> G[Criar conexao com PostgreSQL usando SQLAlchemy]
    G --> H[Funcao buscar_dados_commodities - simbolo, periodo, intervalo]
    H --> I[Usar yfinance para obter historico de precos]
    I --> J[Selecionar coluna Close e adicionar coluna simbolo]
    J --> K[Retornar DataFrame]
    K --> L[Funcao buscar_todos_os_dados_commodities - lista]
    L --> M[Para cada simbolo na lista de commodities, chamar buscar_dados_commodities]
    M --> N[Concatenar todos DataFrames]
    N --> O[Funcao salvar_no_postgres - df, schema]
    O --> P[Salvar DataFrame no PostgreSQL, tabela commodities, substituindo dados]
    P --> Q[Fim]
