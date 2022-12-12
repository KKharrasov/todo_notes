from core.db import engine
from fastapi import FastAPI
from routes import routes
import uvicorn
from user import models


models.Base.metadata.create_all(bind=engine)


def run_app():
    app = FastAPI()
    app.include_router(routes)
    return app


if __name__ == '__main__':
    uvicorn.run('main:app',
                host='127.0.0.1',
                port=8000,
                )
else:
    app = run_app()
