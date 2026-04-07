from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

posts = [
    {
        "id": 1,
        "titulo": "Meu primeiro post",
        "resumo": "Resumo...",
        "conteudo": "Conteúdo completo...",
        "autor": "Carlos"
    },

    {
        "id": 2,
        "titulo": "Namoro Johtrina",
        "resumo": "Jonatan e katrina se assumem",
        "conteudo": "Na tarde dessa terça, katrina como o homem da relação pede Jonatan em namoro e o mesmo aceita causando choque em 0 pessoas",
        "autor": "Laurinha Safadinha"
    }
]

@app.get("/index", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"posts": posts}
    )

@app.get("/post/{id}", response_class=HTMLResponse)
async def visualizar_post(request: Request, id: int):
    
    # Procurar o post pelo id
    post_encontrado = None
    for post in posts:
        if post["id"] == id:
            post_encontrado = post
            break

    # Se não encontrar
    if post_encontrado is None:
        return HTMLResponse(content="Post não encontrado", status_code=404)

    # Se encontrar, renderiza o template
    return templates.TemplateResponse(
        request=request,
        name="post.html",
        context={"post": post_encontrado}
    )