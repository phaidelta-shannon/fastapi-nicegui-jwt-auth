from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import engine, Base, SessionLocal
from .models import User
from .auth import create_access_token, authenticate_user, get_db, get_password_hash, get_current_user
from datetime import timedelta

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(password)
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    return {"message": "User registered successfully"}

@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": token, "token_type": "bearer"}

@app.get("/protected-route")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, you have accessed a protected route!"}