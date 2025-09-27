import streamlit as st

def show_documentation():
    st.title("Documentação da Aplicação")
    st.markdown("""
    ### 1. Visão Geral da Arquitetura
    A aplicação utiliza uma arquitetura de microsserviços, com cada componente rodando em um container Docker separado, facilitando o desenvolvimento e a implantação. A comunicação entre os serviços é feita por meio de uma rede Docker interna.

    - **Backend (API):** Uma API RESTful construída com **FastAPI** em Python. É responsável por toda a lógica de negócio, incluindo as operações de CRUD (Criar, Ler, Atualizar, Deletar) para as tarefas.
    - **Banco de Dados:** Utiliza o **PostgreSQL**, um banco de dados relacional robusto. Ele armazena as informações das tarefas, como título, descrição e status.
    - **Frontend (Interface do Usuário):** Uma interface web interativa desenvolvida com **Streamlit** em Python. O frontend se comunica com o backend através de chamadas HTTP para gerenciar as tarefas.

    ---

    ### 2. Ferramentas e Tecnologias
    | Categoria | Ferramenta/Tecnologia | Descrição |
    | :--- | :--- | :--- |
    | **Orquestração** | **Docker** e **Docker Compose** | Gerenciam o ambiente de desenvolvimento, permitindo que os três serviços rodem de forma isolada. |
    | **Backend** | **FastAPI** | Um framework web moderno e de alta performance para APIs em Python. |
    | **Banco de Dados** | **PostgreSQL** | Um sistema de gerenciamento de banco de dados (SGBD) de código aberto. |
    | **Frontend** | **Streamlit** | Uma biblioteca Python para construir aplicativos web de forma rápida. |
    | **Dependências** | `uvicorn`, `psycopg2-binary`, `requests` | **Uvicorn** (servidor ASGI), **Psycopg2** (adaptador PostgreSQL) e **Requests** (requisições HTTP). |

    ---

    ### 3. Execução e Instalação
    Para rodar a aplicação, siga estes passos.

    **Pré-requisitos:**
    - **Docker** e **Docker Compose** instalados.

    **Estrutura de Diretórios:**
    ```
    .
    ├── Backend/
    │   ├── main.py
    │   ├── Dockerfile
    │   └── requirements.txt
    ├── Frontend/
    │   ├── Home.py
    │   ├── pages/
    │   │   └── docs.py
    │   ├── Dockerfile
    │   └── requirements.txt
    ├── docker-compose.yml
    └── README.md
    ```

    **Passos de Execução:**

    1.  **Navegue até o diretório raiz** (`TodoAPP`).
    2.  **Execute o Docker Compose:**
        ```bash
        docker-compose up --build -d
        ```
    3.  **Acesse a Aplicação:**
        Abra seu navegador e acesse `http://localhost:8501`.
    """, unsafe_allow_html=True)

show_documentation()