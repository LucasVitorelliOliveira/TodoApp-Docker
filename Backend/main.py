from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

# --- Configurações do Banco de Dados ---
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "postgres")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "1234")

# --- Modelos Pydantic para as Tarefas ---
class TaskBase(BaseModel):
    title: str
    description: str | None = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    completed: bool = False
    class Config:
        from_attributes = True

# --- Funções para Conexão com o Banco de Dados ---
def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except psycopg2.OperationalError as e:
        raise HTTPException(status_code=500, detail=f"Erro de conexão com o banco de dados: {e}")

def create_tasks_table():
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT FALSE
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()

# Garante que a tabela seja criada na inicialização da API
create_tasks_table()

# --- Endpoints da API ---

@app.get("/")
def read_root():
    # Endpoint para verificar a conexão com o banco de dados.
    try:
        conn = get_db_connection()
        conn.close()
        return {"status": "Conectado ao banco de dados!"}
    except HTTPException:
        return {"status": "Erro ao conectar ao banco de dados."}

@app.post("/tasks/", response_model=Task, status_code=201)
def create_task(task: TaskCreate):
    # Cria uma nova tarefa no banco de dados.
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description) VALUES (%s, %s) RETURNING id, title, description, completed;",
        (task.title, task.description)
    )
    new_task_tuple = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if new_task_tuple is None:
        raise HTTPException(status_code=500, detail="Erro ao criar a tarefa.")

    new_task_dict = {
        "id": new_task_tuple[0],
        "title": new_task_tuple[1],
        "description": new_task_tuple[2],
        "completed": new_task_tuple[3]
    }
    
    return new_task_dict

@app.get("/tasks/", response_model=list[Task])
def get_tasks():
    # Lista todas as tarefas existentes.
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, completed FROM tasks ORDER BY id;")
    tasks_tuples = cursor.fetchall()
    cursor.close()
    conn.close()

    tasks_list = []
    for t in tasks_tuples:
        tasks_list.append({
            "id": t[0],
            "title": t[1],
            "description": t[2],
            "completed": t[3]
        })
    return tasks_list

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    # Busca uma única tarefa pelo ID.
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, completed FROM tasks WHERE id = %s;", (task_id,))
    task_tuple = cursor.fetchone()
    cursor.close()
    conn.close()

    if task_tuple is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    task_dict = {
        "id": task_tuple[0],
        "title": task_tuple[1],
        "description": task_tuple[2],
        "completed": task_tuple[3]
    }
    return task_dict

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: TaskCreate):
    # Atualiza uma tarefa existente pelo ID.
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET title = %s, description = %s WHERE id = %s RETURNING id, title, description, completed;",
        (task.title, task.description, task_id)
    )
    updated_task_tuple = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if updated_task_tuple is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    updated_task_dict = {
        "id": updated_task_tuple[0],
        "title": updated_task_tuple[1],
        "description": updated_task_tuple[2],
        "completed": updated_task_tuple[3]
    }
    return updated_task_dict

# Endpoint para alternar o status de uma tarefa (completa/incompleta)
@app.patch("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Obter o status atual da tarefa
    cursor.execute("SELECT completed FROM tasks WHERE id = %s;", (task_id,))
    current_status = cursor.fetchone()
    
    if current_status is None:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    new_status = not current_status[0]  # Inverte o status
    
    # 2. Atualizar o status da tarefa
    cursor.execute(
        "UPDATE tasks SET completed = %s WHERE id = %s RETURNING id, title, description, completed;",
        (new_status, task_id)
    )
    
    updated_task_tuple = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()

    if updated_task_tuple is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    
    updated_task_dict = {
        "id": updated_task_tuple[0],
        "title": updated_task_tuple[1],
        "description": updated_task_tuple[2],
        "completed": updated_task_tuple[3]
    }
    return updated_task_dict

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    # Deleta uma tarefa pelo ID.
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s RETURNING id;", (task_id,))
    deleted_task = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    if deleted_task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")