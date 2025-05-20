# app_estoque.py
import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# --- Configuração do banco ---
engine = create_engine("sqlite:///estoque.db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    quantidade = Column(Integer, default=0)
    em_falta = Column(Boolean, default=False)

Base.metadata.create_all(engine)

# --- Interface Streamlit ---
st.title("📦 Controle de Estoque")

menu = st.sidebar.selectbox("Menu", ["Adicionar Produto", "Visualizar Estoque", "Atualizar Estoque"])

# --- Adicionar Produto ---
if menu == "Adicionar Produto":
    nome = st.text_input("Nome do produto")
    quantidade = st.number_input("Quantidade", min_value=0, step=1)

    if st.button("Adicionar"):
        if nome:
            novo = Produto(nome=nome, quantidade=quantidade)
            session.add(novo)
            session.commit()
            st.success(f"Produto '{nome}' adicionado!")
        else:
            st.warning("Informe o nome do produto.")

# --- Visualizar Estoque ---
elif menu == "Visualizar Estoque":
    produtos = session.query(Produto).all()
    if produtos:
        for p in produtos:
            st.write(f"**{p.nome}** | Quantidade: {p.quantidade} | {'❌ Em falta' if p.em_falta else '✅ Disponível'}")
    else:
        st.info("Nenhum produto cadastrado.")

# --- Atualizar Estoque ---
elif menu == "Atualizar Estoque":
    produtos = session.query(Produto).all()
    if produtos:
        produto_nomes = [f"{p.id} - {p.nome}" for p in produtos]
        escolha = st.selectbox("Selecione um produto", produto_nomes)
        produto_id = int(escolha.split(" - ")[0])
        produto = session.query(Produto).get(produto_id)

        nova_qtd = st.number_input("Nova quantidade", value=produto.quantidade, step=1)
        em_falta = st.checkbox("Marcar como em falta", value=produto.em_falta)

        if st.button("Atualizar"):
            produto.quantidade = nova_qtd
            produto.em_falta = em_falta
            session.commit()
            st.success(f"Produto '{produto.nome}' atualizado!")
    else:
        st.info("Nenhum produto para atualizar.")
