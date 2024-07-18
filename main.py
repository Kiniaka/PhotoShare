from fastapi import FastAPI

from src.routes import images
# from src.routes import users
from src.routes import auth

app = FastAPI()

app.include_router(images.router, prefix='/api')
# app.include_router(users.router, prefix='/api')
app.include_router(auth.router, prefix='/api')


@app.get('/')
def read_root():
    return {'message': 'Welcome to PhotoShare!'}
