from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from auth import create_access_token, verify_access_token
from models import Base, Token, UserCreate, TodoCreate, TodoOut
from users import create_user, get_user, authenticate_user
from todos import create_todo, get_todos, update_todo_title, delete_todo
import time

Base.metadata.create_all(engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.middleware("http")
async def loggin_in(request : Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    processed_time = time.time() - start_time
    print(f"{request.method} {request.url.path} completed in {processed_time:.2f} seconds")
    return response

@app.post("/signup")
async def signup(user:UserCreate, db:Session = Depends(get_db)):
    if get_user(db, user.email):
        raise HTTPException(status_code=400, detail="User Already Exists")
    create_user(db, user)
    return {"message": "User Created Successfully"}

@app.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token:str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    username = verify_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid Token")
    user = get_user(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")
    return user

@app.post("/todos", response_model=TodoOut)
async def add_todo(todo:TodoCreate, current_user = Depends(get_current_user), db:Session = Depends(get_db)):
    return create_todo(db, todo, current_user.id)

@app.get("/todos", response_model=list[TodoOut])
async def get_all_todos(current_user = Depends(get_current_user), db:Session = Depends(get_db)):
    return get_todos(db, current_user.id)

@app.put("/todos/{todo_id}", response_model=TodoOut)
async def update_todo(todo_id:int, new_title: str, current_user = Depends(get_current_user), db:Session = Depends(get_db)):
    return update_todo_title(db, todo_id, current_user.id, new_title)

@app.delete("/todos/{todo_id}")
async def remove_todo(todo_id:int, current_user = Depends(get_current_user), db:Session = Depends(get_db)):
    return delete_todo(db, todo_id, current_user.id)

@app.get("/health")
def health():
    return {"Status" : "OK"}