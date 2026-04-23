from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import mysql.connector

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="forum"
    )

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True) #faz com que os dados venham em formato de dicionário

    cursor.execute("SELECT * FROM posts")#pega todos os dados da tabela
    posts = cursor.fetchall()#traz todos os resultados e guarda na variável

    cursor.close()
    conexao.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "posts": posts}
    )


@app.get("/post/{id}", response_class=HTMLResponse)
async def visualizar_post(request: Request, id: int):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()#pega apenas UM resultado da consulta SQL

    cursor.close()
    conexao.close()

    return templates.TemplateResponse(
        request=request,
        name="post.html",
        context={"request": request, "post": post}
    )

@app.get("/create", response_class=HTMLResponse)
async def pagina_create(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create.html",
        context={"request": request}
    )


@app.post("/create")
async def adicionar(request: Request):
    form = await request.form()

    id_str = form.get("id")
    if not id_str:
        return RedirectResponse(url="/", status_code=303)

    id = int(id_str)

    conexao = conectar()
    cursor = conexao.cursor()

    sql = "INSERT INTO posts (id, titulo, resumo, conteudo, autor) VALUES (%s, %s, %s, %s, %s)"
    valores = (
        id,
        form.get("titulo"),
        form.get("resumo"),
        form.get("conteudo"),
        form.get("autor")
    )

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()

    return RedirectResponse(url="/", status_code=303)


@app.get("/edit/{id}", response_class=HTMLResponse)
async def editar_post(request: Request, id: int):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()

    cursor.close()
    conexao.close()

    if not post:
        return RedirectResponse(url="/", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"request": request, "post": post}
    )


@app.post("/edit/{id}")
async def edit_post(request: Request, id: int):
    form = await request.form()

    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE posts
    SET titulo=%s, resumo=%s, conteudo=%s, autor=%s
    WHERE id=%s
    """

    valores = (
        form.get("titulo"),
        form.get("resumo"),
        form.get("conteudo"),
        form.get("autor"),
        id
    )

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()

    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{id}")
async def delete_post(id: int):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
    conexao.commit()

    cursor.close()
    conexao.close()

    return RedirectResponse(url="/", status_code=303)