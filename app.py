import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Dashboard de Finanças Pessoais", layout="wide")
st.markdown("""
    <style>
    .main {
        background-color: #0f0f0f;
        color: #f0f0f0;
    }
    h1, h2, h3 {
        color: #39ff14;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Dashboard de Finanças Pessoais")

st.sidebar.header("Adicionar Transação")
tipo = st.sidebar.selectbox("Tipo de transação", ["Entrada", "Saída"])
data = st.sidebar.date_input("Data", datetime.today())
categoria = st.sidebar.selectbox("Categoria", [
    "Salário", "Mercado", "Escola", "Energia Elétrica", "Água",
    "Internet e Telefone", "Gasolina", "Cartão de Crédito", "Gastos Extras"
])
valor = st.sidebar.number_input("Valor", min_value=0.0, format="%.2f")
descricao = st.sidebar.text_input("Descrição (opcional)")

if 'transacoes' not in st.session_state:
    st.session_state.transacoes = pd.DataFrame(columns=["Data", "Tipo", "Categoria", "Valor", "Descrição"])

if st.sidebar.button("Adicionar"):
    nova_transacao = {
        "Data": data,
        "Tipo": tipo,
        "Categoria": categoria,
        "Valor": valor,
        "Descrição": descricao
    }
    st.session_state.transacoes = pd.concat([st.session_state.transacoes, pd.DataFrame([nova_transacao])], ignore_index=True)
    st.success("Transação adicionada com sucesso!")

st.subheader("📅 Histórico de Transações")
st.dataframe(st.session_state.transacoes.style.set_properties(**{
    'background-color': '#1a1a1a',
    'color': '#f0f0f0'
}))

# Resumo financeiro
st.subheader("💰 Resumo Financeiro")
entrada_total = st.session_state.transacoes[st.session_state.transacoes['Tipo'] == 'Entrada']['Valor'].sum()
saida_total = st.session_state.transacoes[st.session_state.transacoes['Tipo'] == 'Saída']['Valor'].sum()
saldo = entrada_total - saida_total

col1, col2, col3 = st.columns(3)
col1.metric("Entradas", f"R$ {entrada_total:.2f}", delta_color="normal")
col2.metric("Saídas", f"R$ {saida_total:.2f}", delta_color="inverse")
col3.metric("Saldo Atual", f"R$ {saldo:.2f}", delta_color="off")

# Gráficos
st.subheader("📈 Visualizações")
gasto_categoria = st.session_state.transacoes[st.session_state.transacoes['Tipo'] == 'Saída'].groupby('Categoria')['Valor'].sum().reset_index()

fig_pizza = px.pie(gasto_categoria, names='Categoria', values='Valor', title='Distribuição de Gastos por Categoria',
                   color_discrete_sequence=px.colors.sequential.Emrld)
st.plotly_chart(fig_pizza, use_container_width=True)

transacoes_por_data = st.session_state.transacoes.groupby(['Data', 'Tipo'])['Valor'].sum().reset_index()
fig_linha = px.line(transacoes_por_data, x='Data', y='Valor', color='Tipo', title='Entradas e Saídas ao Longo do Tempo',
                    color_discrete_map={'Entrada': '#39ff14', 'Saída': '#ff073a'})
st.plotly_chart(fig_linha, use_container_width=True)

st.markdown("""
    <hr style="border-top: 2px solid #39ff14;">
    <p style="color:#808080; text-align:center;">Feito com ❤️ usando Streamlit e Plotly</p>
""", unsafe_allow_html=True)
