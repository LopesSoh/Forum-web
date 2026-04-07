from fastapi import FastAPI, Request, Form
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

    # Se encontrar, renderiza o template
    return templates.TemplateResponse(
        request=request,
        name="post.html",
        context={"post": post_encontrado}
    )

# MOSTRA A PÁGINA
@app.get("/create")
async def pagina_create(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create.html",
        context={"request": request}
    )

# RECEBE O FORM
@app.post("/create")
async def adicionar(request: Request):
    form = await request.form()

    id_str = form.get("id")

    if not id_str:
        return RedirectResponse(url="/index", status_code=303)

    id = int(id_str)

    for post in posts:
        if post["id"] == id:
            return RedirectResponse(url="/index", status_code=303)

    posts.append({
        "id": id,
        "titulo": form.get("titulo"),
        "resumo": form.get("resumo"),
        "conteudo": form.get("conteudo"),
        "autor": form.get("autor")
    })

    return RedirectResponse(url="/index", status_code=303)

# MOSTRA A PÁGINA
@app.get("/edit/{id}")
async def editar_post(request: Request, id: int):

    post_encontrado = None
    for post in posts:
        if post["id"] == id:
            post_encontrado = post
            break

    if not post_encontrado:
        return RedirectResponse(url="/index", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"post": post_encontrado}
    )

@app.post("/edit/{id}")
async def edit_post(request: Request, id: int):
    form = await request.form()

    post = next((p for p in posts if p["id"] == id), None)

    if post:
        post["titulo"] = form.get("titulo")
        post["resumo"] = form.get("resumo")
        post["conteudo"] = form.get("conteudo")
        post["autor"] = form.get("autor")

    return RedirectResponse(url="/index", status_code=303)

@app.post("/delete/{id}")
async def delete_post(id: int):
    global posts
    posts = [p for p in posts if p["id"] != id]

    return RedirectResponse(url="/index", status_code=303)