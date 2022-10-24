from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from app.routers import items

app = FastAPI(title="Fast API")
app.add_middleware(
    CORSMiddleware,
    allow_origins="*"
)


@app.middleware("http")
def logger(req: Request, call_next):
    print("[" + req.method + "] - " + str(req.url))
    return call_next(req)


app.include_router(items.router)

