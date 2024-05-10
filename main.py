
import databaseHandling
from fastapi import FastAPI
from router import router
import uvicorn

app = FastAPI()
app.include_router(router)


if __name__ == "__main__":
    databaseHandling.databaseInit()
    uvicorn.run(app, host = "127.0.0.1", port = 8080) #localhost
    databaseHandling.closeDatabase()
