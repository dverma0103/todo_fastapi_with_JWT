# FastAPI Todo App with JWT

## Setup
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Endpoints
-POST `/Signup`
-POST `/Login`
-GET `/Todos`
-POST `/Todos`
-PUT `/Todos/{id}`
-DELETE `/Todos/{id}`
-GET `/health`

## Depolyement
-Push to GitHub
-Deploy on Render
```bash
Start Command: uvicorn main:app --host=0.0.0.0 --port=10000
```

Set `.env` variables in deployement panel.