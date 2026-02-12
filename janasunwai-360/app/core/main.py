from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import issues, responses, budgets, officials, auth

app = FastAPI(
    title="JANASUNWAI 360",
    description="Anonymous citizen feedback with transparent government response",
    version="1.0.0"
)


app.mount("/static", StaticFiles(directory="app/static"), name="static")


templates = Jinja2Templates(directory="app/templates")


app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(issues.router, prefix="/issues", tags=["Issues"])
app.include_router(responses.router, prefix="/responses", tags=["Responses"])
app.include_router(budgets.router, prefix="/budgets", tags=["Budgets"])
app.include_router(officials.router, prefix="/officials", tags=["Officials"])


@app.get("/")
def root():
    return {
        "message": "JANASUNWAI 360 backend is running",
        "status": "OK"
    }
