from fastapi import FastAPI

from knowledge_api import middleware

app = FastAPI()

middleware.auth.handle_errors(app=app)
