from fastapi import FastAPI

from src.routes import images, users

app = FastAPI()

app.include_router(images.router, prefix='/api')

@app.get('/')
def read_root():
    return {'message': 'Welcome to PhotoShare!'}