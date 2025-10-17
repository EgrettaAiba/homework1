from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.routers import posts, users

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)


@app.get("/", response_class=HTMLResponse)
def home():
    html_path = Path(__file__).parent / "templates" / "home.html"

    with open(html_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    return HTMLResponse(content=html_content)
