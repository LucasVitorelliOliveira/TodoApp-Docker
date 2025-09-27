import streamlit as st
import requests

# URL base da sua API FastAPI
API_URL = "http://todoapp-backend:8000"

st.set_page_config(page_title="Gerenciador de Tarefas", layout="wide", initial_sidebar_state="collapsed")

# --- Funções para Interagir com a API ---

def get_tasks():
    try:
        response = requests.get(f"{API_URL}/tasks/")
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.ConnectionError:
        st.error("Erro de conexão com a API do backend. Verifique se o container `fastapi-backend` está rodando.")
    return []

def create_task(title, description):
    data = {"title": title, "description": description}
    response = requests.post(f"{API_URL}/tasks/", json=data)
    return response.status_code == 201

def delete_task(task_id):
    response = requests.delete(f"{API_URL}/tasks/{task_id}")
    return response.status_code == 204

def complete_task(task_id):
    response = requests.patch(f"{API_URL}/tasks/{task_id}/complete")
    return response.status_code == 200

def update_task_content(task_id, title, description):
    data = {"title": title, "description": description}
    response = requests.put(f"{API_URL}/tasks/{task_id}", json=data)
    return response.status_code == 200

# --- Interface do Streamlit ---

# Cria uma linha de três colunas para o layout centralizado (30% da tela)
col_left, col_center, col_right = st.columns([0.35, 0.3, 0.35])

with col_center:
    st.title("Organize suas Tarefas")
    st.header("Adicionar Nova Tarefa")
    with st.form(key="add_task_form"):
        title = st.text_input("Título da Tarefa")
        description = st.text_area("Descrição (Opcional)")
        submit_button = st.form_submit_button(label="Adicionar Tarefa")

        if submit_button and title:
            if create_task(title, description):
                st.success("Tarefa adicionada com sucesso!")
                st.rerun()
            else:
                st.error("Erro ao adicionar tarefa.")

    st.header("Minhas Tarefas")

    tasks = get_tasks()
    if tasks:
        st.markdown("---")
        for task in tasks:
            with st.container(border=True):
                # Primeira linha: checkbox e título
                col_check, col_title = st.columns([0.05, 0.95])
                
                with col_check:
                    is_completed = st.checkbox("", value=task['completed'], key=f"checkbox_{task['id']}")
                
                with col_title:
                    task_title_text = f"~~{task['title']}~~" if task['completed'] else task['title']
                    st.markdown(f"**{task_title_text}**", unsafe_allow_html=True)
                    if task['description']:
                        st.caption(task['description'])

                # Segunda linha: botões de ação (editar e deletar)
                col_actions = st.columns([0.5, 0.5])
                
                with col_actions[0]:
                    with st.expander("Editar"):
                        with st.form(key=f"edit_form_{task['id']}", clear_on_submit=False):
                            new_title = st.text_input("Novo Título", value=task['title'], key=f"edit_title_{task['id']}")
                            new_description = st.text_area("Nova Descrição", value=task['description'], key=f"edit_desc_{task['id']}")
                            update_button = st.form_submit_button("Atualizar")

                            if update_button:
                                if update_task_content(task['id'], new_title, new_description):
                                    st.success("Tarefa atualizada!")
                                    st.rerun()
                                else:
                                    st.error("Erro ao atualizar a tarefa.")
                
                with col_actions[1]:
                    if st.button("Deletar", key=f"delete_{task['id']}"):
                        if delete_task(task['id']):
                            st.success("Tarefa deletada!")
                            st.rerun()
                        else:
                            st.error("Erro ao deletar tarefa.")

                # Lógica para atualizar o status do checkbox
                if st.session_state[f"checkbox_{task['id']}"] != task['completed']:
                    if complete_task(task['id']):
                        st.success("Status atualizado!")
                        st.rerun()
                    else:
                        st.error("Erro ao atualizar o status.")
    else:
        st.info("Nenhuma tarefa encontrada. Use o formulário acima para adicionar a primeira!")