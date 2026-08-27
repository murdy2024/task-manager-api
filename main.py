from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import text
from database import engine, SessionLocal 
from models import TaskDB, UserDB
from schemas import Task, TaskResponse, UserCreate, UserResponse
from auth import hash_password, verify_password
from jwt_token import create_access_token, SECRET_KEY, ALGORITHM
import jwt
from jwt import InvalidTokenError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db=Depends(get_db)
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        db_user = db.query(UserDB).filter(
            UserDB.id == int(user_id)
        ).first()

        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        return db_user

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
@app.post('/register', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db = Depends(get_db)):
    existing_user = db.query(UserDB).filter(
    (UserDB.username == user.username) |
    (UserDB.email == user.email)).first()
    if existing_user:
            raise HTTPException(
        status_code=400,
        detail='Username or email already exists')

    hashed_password = hash_password(user.password)
    new_user = UserDB(
        username = user.username,
        email = user.email,
        hashed_password = hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post('/login')
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db = Depends(get_db)
):
    db_user = db.query(UserDB).filter(
        UserDB.username == form_data.username
    ).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )
    if not verify_password(
        form_data.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )
    access_token = create_access_token(
        data={"sub": str(db_user.id)}
    )
    return {
        'access_token': access_token,
        'token_type': 'bearer'
    }
    

@app.get('/db-test')
def db_test():
    with engine.connect() as connection:
        result = connection.execute(text('SELECT version()'))
        return {'database': result.scalar()}


@app.get('/')
def home():
    return {'message': 'Hello World!'}

@app.get('/tasks', response_model=list[TaskResponse])
def get_tasks(
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    tasks_from_db = db.query(TaskDB).filter(
    TaskDB.user_id == current_user.id
).all()
    return tasks_from_db


@app.post('/tasks', response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: Task,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    new_task = TaskDB(
        title = task.title,
        completed = task.completed,
        user_id = current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

@app.get('/tasks/{task_id}', response_model=TaskResponse)
def get_task(
    task_id: int,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    task = db.query(TaskDB).filter(
        TaskDB.id == task_id,
        TaskDB.user_id == current_user.id
    ).first()
    if task:
        return task
    raise HTTPException(status_code=404, detail='Task not found')

@app.delete('/tasks/{task_id}')
def delete_task(
    task_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = db.query(TaskDB).filter(
        TaskDB.id == task_id,
        TaskDB.user_id == current_user.id
    ).first()
    if task:
        db.delete(task)
        db.commit()
        return {'message': 'Task deleted'}
    raise HTTPException(
        status_code=404,
        detail='Task not found'
    )

@app.put('/tasks/{task_id}', response_model=TaskResponse)
def update_task(
    task_id: int,
    updated_task: Task,
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    task = db.query(TaskDB).filter(
        TaskDB.id == task_id,
        TaskDB.user_id == current_user.id
    ).first()
    if task:
        task.title = updated_task.title
        task.completed = updated_task.completed
        db.commit()
        db.refresh(task)
        return task
    raise HTTPException(
        status_code=404,
        detail='Task not found'
    )
