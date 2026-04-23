from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from dao import (
    listar_posts,
    buscar_post,
    inserir_post,
    atualizar_post,
    deletar_post
)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "posts": listar_posts()
        }
    )


@app.get("/post/{id}", response_class=HTMLResponse)
async def ver_post(request: Request, id: int):
    return templates.TemplateResponse(
        request=request,
        name="post.html",
        context={
            "request": request,
            "post": buscar_post(id)
        }
    )


@app.get("/create", response_class=HTMLResponse)
async def pagina_create(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create.html",
        context={"request": request}
    )


@app.post("/create")
async def criar_post(request: Request):
    form = await request.form()

    inserir_post(
        int(form.get("id")),
        form.get("titulo"),
        form.get("resumo"),
        form.get("conteudo"),
        form.get("autor")
    )

    return RedirectResponse(url="/", status_code=303)


@app.get("/edit/{id}", response_class=HTMLResponse)
async def editar_post(request: Request, id: int):
    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={
            "request": request,
            "post": buscar_post(id)
        }
    )


@app.post("/edit/{id}")
async def salvar_edicao(request: Request, id: int):
    form = await request.form()

    atualizar_post(
        id,
        form.get("titulo"),
        form.get("resumo"),
        form.get("conteudo"),
        form.get("autor")
    )

    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{id}")
async def deletar(id: int):
    deletar_post(id)
    return RedirectResponse(url="/", status_code=303)