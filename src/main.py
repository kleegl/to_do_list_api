from fastapi import FastAPI, status

from task_api import task_router
from user_api import user_router


app = FastAPI()


app.include_router(task_router)
app.include_router(user_router)


@app.get("/")
async def health():
    return status.HTTP_200_OK
