# Alunos

***Lucas Vitorelli de Oliveira*** - ***2211600019***

***Mateus Henrique Silva Rizzo*** - ***2211600214***


# Gerenciador de Tarefas com Docker

Uma aplicação completa de gerenciamento de tarefas, com frontend interativo e backend robusto, rodando em containers Docker.

## Visão Geral da Arquitetura

Esta aplicação utiliza uma arquitetura de microsserviços, com cada componente rodando em um container Docker separado. A comunicação entre os serviços é feita através de uma rede Docker interna, garantindo isolamento e escalabilidade.

-   **Backend (API):** Uma API RESTful de alta performance construída com **FastAPI** (Python). Responsável por toda a lógica de negócio e pela comunicação com o banco de dados.
-   **Banco de Dados:** **PostgreSQL**, um sistema de banco de dados relacional que garante a persistência das tarefas.
-   **Frontend (Interface do Usuário):** Uma interface web interativa desenvolvida com **Streamlit** (Python). Ela se comunica com o backend para gerenciar as tarefas.

## Tecnologias e Ferramentas

| Categoria | Ferramenta/Tecnologia | Descrição |
| :--- | :--- | :--- |
| **Orquestração** | **Docker** e **Docker Compose** | Gerenciam o ambiente de desenvolvimento, permitindo que os três serviços rodem de forma isolada. |
| **Backend** | **FastAPI** | Framework web moderno para construir APIs robustas e rápidas. |
| **Banco de Dados** | **PostgreSQL** | SGBD relacional, confiável e de código aberto. |
| **Frontend** | **Streamlit** | Biblioteca Python para criar aplicativos web de forma simples e rápida. |

## Estrutura do Projeto

A aplicação é organizada em diretórios para cada serviço, com um arquivo `docker-compose.yml` na raiz para orquestração.

.
├── Backend/
│   ├── main.py             # Lógica do backend (API)
│   ├── Dockerfile          # Instruções para construir a imagem do backend
│   └── requirements.txt    # Dependências do backend
├── Frontend/
│   ├── Home.py             # Lógica principal do frontend
│   ├── pages/              # Módulo para páginas adicionais
│   │   └── docs.py         # Página de documentação
│   ├── Dockerfile          # Instruções para construir a imagem do frontend
│   └── requirements.txt    # Dependências do frontend
├── docker-compose.yml      # Arquivo para orquestrar os serviços
└── README.md


## Como Rodar a Aplicação

Siga estas instruções para colocar o projeto no ar em seu ambiente local.

### Pré-requisitos
Certifique-se de que você tem o **Docker** e o **Docker Compose** instalados em sua máquina.

### Execução
1.  **Navegue até o diretório raiz** do projeto.
2.  Execute o comando abaixo para construir as imagens e iniciar todos os containers em segundo plano:
    ```bash
    docker-compose up --build -d
    ```

    *O `docker-compose` irá criar a rede interna, subir o banco de dados e, em seguida, o backend e o frontend, garantindo que as dependências estejam na ordem correta.*

3.  Após a execução, a aplicação estará disponível em seu navegador.
    ```
    🌐 Acesse a aplicação em: http://localhost:8501
    ```

### Como Parar a Aplicação
Para parar e remover todos os containers, volumes e redes criados pelo `docker-compose`, use o seguinte comando no diretório raiz:
```bash
docker-compose down -v
O -v é usado para remover também os volumes do banco de dados, garantindo um ambiente limpo para o próximo uso.
