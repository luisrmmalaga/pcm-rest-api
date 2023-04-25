import threading
import time

import schedule
from fastapi import FastAPI

from routes.checkpoint import checkpoint
from routes.favorito import favorito
from routes.logUsuario import logUser
from routes.usuario import user
from tools.dailyUpdateJob import job

app = FastAPI(title="PCM REST API with FastAPI and MongoDB", version= "0.0.1")

app.include_router(user)
app.include_router(logUser)
app.include_router(favorito)
app.include_router(checkpoint)
    

def run_scheduler():

    schedule.every().day.at("18:00", "Europe/Amsterdam").do(job)

    while(True):
        schedule.run_pending()
        time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()
