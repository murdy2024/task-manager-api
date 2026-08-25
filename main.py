from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import text
from database import engine, SessionLocal 
from models import TaskDB
from schemas import Task, TaskResponse
  
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get('/db-test')
def db_test():
    with engine.connect() as connection:
        result = connection.execute(text('SELECT version()'))
        return {'database': result.scalar()}


@app.get('/')
def home():
    return {'message': 'Hello World!'}

@app.get('/tasks', response_model=list[TaskResponse])
def get_tasks(db = Depends(get_db)):
    tasks_from_db = db.query(TaskDB).all()
    return tasks_from_db

@app.post('/tasks', response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: Task, db = Depends(get_db)):
    new_task = TaskDB(
        title = task.title,
        completed = task.completed
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get('/tasks/{task_id}', response_model=TaskResponse)
def get_task(task_id: int, db = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if task:
        return task
    raise HTTPException (status_code = 404, detail='Task not found')

@app.delete('/tasks/{task_id}')
def delete_task(task_id: int,db = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        return {'message': 'Task deleted'}
    raise HTTPException(status_code=404, detail='Task not found')

@app.put('/tasks/{task_id}', response_model=TaskResponse)
def update_task(task_id: int, updated_task: Task, db = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if task:
        task.title = updated_task.title
        task.completed = updated_task.completed
        db.commit()
        db.refresh(task)
        return task
    raise HTTPException(status_code=404, detail='Task not found')
