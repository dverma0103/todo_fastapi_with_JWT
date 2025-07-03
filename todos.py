from sqlalchemy.orm import Session
from models import TodoCreate, Todo

def create_todo(db:Session, todo:TodoCreate, user_id:int):
    todo_db = Todo(owner_id = user_id, title = todo.title, completed = todo.completed)
    db.add(todo_db)
    db.commit()
    db.refresh(todo_db)
    return todo_db

def get_todos(db:Session, user_id:int):
    return db.query(Todo).filter(Todo.owner_id == user_id).all()

def update_todo_title(db:Session, todo_id:int, user_id:int, new_title:str):
    todo = db.query(Todo).filter(Todo.owner_id == user_id, Todo.id == todo_id).first()
    if todo:
        todo.title = new_title
        db.commit()
    return todo

def delete_todo(db:Session, todo_id:int, user_id:int):
    todo = db.query(Todo).filter(Todo.owner_id == user_id, Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
    return "Todo Successfully Deleted"