from tempfile import template
from fastapi import FastAPI
from dotenv import load_dotenv
from app.services.supabase import supabase
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.staticfiles import StaticFiles

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="app/template")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.route("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html",site_name="Janasunwai",
        tagline="Speak Up Anonymously. Track Government Actions Transparently",
        context={"request": request})

@app.route("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html",site_name="Janasunwai",
        tagline="Speak Up Anonymously. Track Government Actions Transparently",
        context={"request": request})

@app.route("/submit_issue")
async def submit_issue(request: Request):
    return templates.TemplateResponse("submit_issue.html",site_name="Janasunwai",
        tagline="Speak Up Anonymously. Track Government Actions Transparently",
        context={"request": request})

@app.route("/public_issues")
async def public_issues(request: Request):
    return templates.TemplateResponse("public_issues.html",site_name="Janasunwai",
        tagline="Speak Up Anonymously. Track Government Actions Transparently",
        context={"request": request})

@app.route("/government_response")
async def government_response(request: Request):
    return templates.TemplateResponse("government_response.html",site_name="Janasunwai",
        tagline="Speak Up Anonymously. Track Government Actions Transparently",
        context={"request": request})

@app.route("/budget_tracker")
async def budget_tracker(request: Request):
    return templates.TemplateResponse("budget_tracker.html",site_name="Janasunwai",
        tagline="Speak Up Anonymously. Track Government Actions Transparently",
        context={"request": request})

@app.route("/about")
async def about(request: Request):
    return template.TemplateResponse("about.html",site_name="Janasunwai",
        tagline="Speak Up Anonymously. Track Government Actions Transparently",
        context={"request": request})

@app.get("/issues")
def issue_list():
    data = supabase.table("issues").select("*").execute()
    return data.data

# @app.post("/issues")
# def submit_issue(issue_data: dict):
#     response = supabase.table("issues").insert(issue_data).execute()
#     return {
#         "message": "Issue submitted successfully",
#         "data": response.data
#     }

# @app.put("/issues/{issue_id}")
# def update_issue(issue_id: str, issue_data: dict):
#     response = (
#         supabase
#         .table("issues")
#         .update(issue_data)
#         .eq("id", issue_id)
#         .execute()
#     )
#     return {
#         "message": "Issue updated successfully",
#         "data": response.data
#     }

@app.get("/")
def root():
    return {"status": "JANASUNWAI 360 running"}
