from model import conectar

def listar_posts():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()

    cursor.close()
    conexao.close()

    return posts


def buscar_post(id):
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    post = cursor.fetchone()

    cursor.close()
    conexao.close()

    return post


def inserir_post(id, titulo, resumo, conteudo, autor):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    INSERT INTO posts (id, titulo, resumo, conteudo, autor)
    VALUES (%s, %s, %s, %s, %s)
    """

    valores = (id, titulo, resumo, conteudo, autor)

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()


def atualizar_post(id, titulo, resumo, conteudo, autor):
    conexao = conectar()
    cursor = conexao.cursor()

    sql = """
    UPDATE posts
    SET titulo=%s, resumo=%s, conteudo=%s, autor=%s
    WHERE id=%s
    """

    valores = (titulo, resumo, conteudo, autor, id)

    cursor.execute(sql, valores)
    conexao.commit()

    cursor.close()
    conexao.close()


def deletar_post(id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
    conexao.commit()

    cursor.close()
    conexao.close()