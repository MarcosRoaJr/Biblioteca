from flask_mysqldb import MySQL

mysql = MySQL()

def init_app(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_PORT'] = 3306
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = 'biblioteca_virtual'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    mysql.init_app(app)
    return mysql

# ==================BUSCAS DADOS=================

# Cara aqui vai procura o id do livro e retorna os generos do livro
def retornar_idgenero(identificador: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM livro_genero WHERE id_livro = %s;", (identificador,))
    row = conectar.fetchall()
    conectar.close()
    return [r["id_genero"] for r in row]

# Aqui retorna o id da editora
def retornar_ideditora(identificador: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM livro WHERE id_livro = %s;", (identificador,))
    row = conectar.fetchone()
    conectar.close()
    return row["id_editora"] if row else None

def buscar_editora_id(identificador: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM editora WHERE id_editora = %s;", (identificador,))
    row = conectar.fetchone()
    conectar.close()
    return row["Nome"] if row else None

def retornar_idisbn(identificador: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM livro WHERE ISBN = %s;", (identificador,))
    row = conectar.fetchone()
    conectar.close()
    return row["id_livro"] if row else None

def buscar_genero(identificador: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM genero WHERE id_genero = %s;", (identificador,))
    row = conectar.fetchone()
    conectar.close()
    return row

def buscar_todos_emprestimos():
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM emprestimo;")
    rows = conectar.fetchall()
    conectar.close()
    return rows

def buscar_numeropatrimonio_por_emprestimo(identificador: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT id_emprestimo FROM emprestimo WHERE id_emprestimo = %s;", (identificador,))
    row = conectar.fetchone()
    conectar.close()

    conectar = mysql.connection.cursor()
    conectar.execute("SELECT id_numero_patrimonio FROM livro_emprestimo WHERE id_emprestimo = %s;", (row,))
    row = conectar.fetchone()
    conectar.close()
    return row["id_emprestimo"] if row else None

def buscar_livro_por_patrimonio(identificador: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT id_livro FROM exemplares WHERE id_numero_patrimonio = %s;", (identificador,))
    row = conectar.fetchone()
    conectar.close()
    return row["id_livro"] if row else None


def buscar_todos_livrosemprestados():
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM livro_emprestimo;")
    rows = conectar.fetchall()
    conectar.close()
    return rows

def buscar_todos_livrosemprestados():
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM livro_emprestimo;")
    rows = conectar.fetchall()
    conectar.close()
    return rows

def buscar_todos_generos():
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM genero;")
    rows = conectar.fetchall()
    conectar.close()
    return rows

def buscar_todos_autores():
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM autor;")
    rows = conectar.fetchall()
    conectar.close()
    return rows

def buscar_todos_livros():
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM livro;")
    rows = conectar.fetchall()
    conectar.close()
    return rows

def buscar_todos_usuario():
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM usuarios;")
    rows = conectar.fetchall()
    conectar.close()
    return rows

def buscar_todos_exemplares():
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM exemplares;")
    rows = conectar.fetchall()
    conectar.close()
    return rows

def formatar_isbn(isbn: str) -> str:
    if not isbn:
        return isbn
    # garante que é string
    isbn = str(isbn)
    return f"{isbn[0:3]}-{isbn[3:5]}-{isbn[5:10]}-{isbn[10:12]}"


# Busca as informações do usuario
# função em potencial para trocar o nome, ver depois de não é ideal ver a troca dos nomes
def verificar_usuario_id(usuario_id, senha):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM usuarios WHERE id_usuario = %s; ", (usuario_id,))
    listar = conectar.fetchone()
    conectar.close()

    if not listar:
        return None
    return listar if listar['senha'] == senha else None

def verificar_usuario_nome(usuario, senha):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM usuarios WHERE nome = %s; ", (usuario,))
    listar = conectar.fetchone()
    conectar.close()

    if not listar:
        return None
    return listar if listar['senha'] == senha else None

# Busca os livros por ID
def buscar_livro_id(id_livro: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM livro WHERE id_livro = %s;", (id_livro,))
    listar = conectar.fetchone()
    conectar.close()

    if listar and listar.get("ISBN"):
        listar["ISBN"] = formatar_isbn(listar["ISBN"])
    return listar

# Aqui ele busca livros pelo nome junto com o select
def buscar_livro_nome():
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM livro;")
    listar_lvr = conectar.fetchall()
    conectar.close()

    for r in listar_lvr:
        if r.get("ISBN"):
            r["ISBN"] = formatar_isbn(r["ISBN"])
    return listar_lvr

def buscar_status_nome():
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT status_emprestimo FROM emprestimo;")
    listar_lvr = conectar.fetchall()
    conectar.close()
    
    return listar_lvr

def buscar_livro_isbn(identificador: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT l.id_livro, l.titulo, l.ISBN, DATE_FORMAT(l.data_publicacao,'%%d/%%m/%%Y') AS data_publicacao, e.Nome AS editora, IFNULL(GROUP_CONCAT(DISTINCT CONCAT(a.nome,' ',a.sobrenome) ORDER BY a.sobrenome SEPARATOR ', '),'—') AS autores, IFNULL(GROUP_CONCAT(DISTINCT g.genero ORDER BY g.genero SEPARATOR ', '),'—') AS generos, COUNT(DISTINCT ex.numero_exemplar) AS qtd_exemplares, IFNULL(GROUP_CONCAT(DISTINCT ex.etiqueta ORDER BY ex.numero_exemplar SEPARATOR ', '),'—') AS etiquetas, IFNULL(pl.setor,'—') AS setor, IFNULL(pl.estante,'—') AS estante, IFNULL(loc.nome,'—') AS campus FROM livro l JOIN editora e ON l.id_editora = e.id_editora LEFT JOIN livro_autor la ON l.id_livro = la.id_livro LEFT JOIN autor a ON la.id_autor = a.id_autor LEFT JOIN livro_genero lg ON l.id_livro = lg.id_livro LEFT JOIN genero g ON lg.id_genero = g.id_genero LEFT JOIN exemplares ex ON l.id_livro = ex.id_livro LEFT JOIN posicao_livro pl ON l.id_livro = pl.id_livro LEFT JOIN localidade_livro loc ON pl.id_campus = loc.id_campus WHERE l.ISBN = %s GROUP BY l.id_livro, l.titulo, l.ISBN, data_publicacao, editora, setor, estante, campus;",(identificador,))
    listar = conectar.fetchone()
    conectar.close()

    if listar and listar.get("ISBN"):
        listar["ISBN"] = formatar_isbn(listar["ISBN"])
    return listar

# chamar a tabela toda da localidade do livro depois achar o câmpus que ele está com outra função

def buscar_locallivro(id_livro: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM posicao_livro WHERE id_livro = %s;", (id_livro,))
    listar = conectar.fetchone()
    conectar.close()

    return listar

def buscar_campus_id(id_capus: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM localidade_livro WHERE id_campus = %s", (id_capus,))
    listar = conectar.fetchone()
    conectar.close()

    return listar

def buscar_campus():
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM localidade_livro")
    listar = conectar.fetchall()
    conectar.close()

    return listar


# =================Inserir dados=================

def criar_usuario(nome, data_nascimento, email, cpf, telefone, senha, nivel_acesso):
    conectar = mysql.connection.cursor()
    conectar.execute("INSERT INTO usuarios (nome, data_nascimento, email, cpf, telefone, senha, nivel_acesso) VALUES (%s, %s, %s , %s, %s, %s, %s)", (nome, data_nascimento, email, cpf, telefone, senha, nivel_acesso,)) 
    mysql.connection.commit()
    conectar.close()

def validar_usuario(email_info,cpf_info):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT email, cpf FROM usuarios WHERE email = %s OR cpf = %s", (email_info, cpf_info,))
    existe = conectar.fetchone()
    conectar.close()

    return existe

def criar_posicaolivro(setor, estante, id_campus, id_livro):
    conectar = mysql.connection.cursor()
    conectar.execute("INSERT INTO posicao_livro (setor, estante, id_campus, id_livro) VALUES (%s, %s, %s, %s)",(setor, estante, id_campus, id_livro))
    mysql.connection.commit()
    conectar.close()
# ==================FIM=================

# Rota para buscar emprestimos
# aprendi a usar o Join

def buscar_emprestimo(identificador: int):
    conectar = mysql.connection.cursor()
    sql = "SELECT e.id_emprestimo, u.nome AS usuario, l.titulo AS livro, ex.numero_exemplar, ex.etiqueta, e.data_saida, e.hora_saida, e.data_prevista_devolucao, e.status_emprestimo, e.data_devolucao FROM emprestimo e JOIN usuarios u ON u.id_usuario = e.id_usuario JOIN livro_emprestimo le ON le.id_emprestimo = e.id_emprestimo JOIN exemplares ex ON ex.numero_patrimonio = le.id_numero_patrimonio JOIN livro l ON l.id_livro = ex.id_livro WHERE e.id_emprestimo = %s ORDER BY e.id_emprestimo, ex.numero_exemplar;"
    conectar.execute(sql, (identificador,))
    emprestimo = conectar.fetchall()
    conectar.close()

    return emprestimo
    
def buscar_emprestimo_por_livro(identificador: int):
    conectar = mysql.connection.cursor()
    sql = "SELECT e.id_emprestimo, u.nome AS usuario, l.titulo AS livro, ex.numero_exemplar, ex.etiqueta, e.data_saida, e.hora_saida, e.data_prevista_devolucao, e.status_emprestimo, e.data_devolucao FROM emprestimo e JOIN usuarios u ON u.id_usuario = e.id_usuario JOIN livro_emprestimo le ON le.id_emprestimo = e.id_emprestimo JOIN exemplares ex ON ex.numero_patrimonio = le.id_numero_patrimonio JOIN livro l ON l.id_livro = ex.id_livro WHERE l.id_livro = %s ORDER BY e.id_emprestimo, ex.numero_exemplar;"
    conectar.execute(sql, (identificador,))
    emprestimo = conectar.fetchall()
    conectar.close()

    return emprestimo

def buscar_emprestimo_por_usuario(identificador: int):
    conectar = mysql.connection.cursor()
    sql = "SELECT e.id_emprestimo, u.nome AS usuario, l.titulo AS livro, ex.numero_exemplar, ex.etiqueta, e.data_saida, e.hora_saida, e.data_prevista_devolucao, e.status_emprestimo, e.data_devolucao FROM emprestimo e JOIN usuarios u ON u.id_usuario = e.id_usuario JOIN livro_emprestimo le ON le.id_emprestimo = e.id_emprestimo JOIN exemplares ex ON ex.numero_patrimonio = le.id_numero_patrimonio JOIN livro l ON l.id_livro = ex.id_livro WHERE u.id_usuario = %s ORDER BY e.id_emprestimo, ex.numero_exemplar;"
    conectar.execute(sql, (identificador,))
    emprestimo = conectar.fetchall()
    conectar.close()

    return emprestimo

def atualizar_usuario(id_usuario, **campos):
    conectar = mysql.connection.cursor()

    colunas = ", ".join([f"{k} = %s" for k in campos.keys()])
    valores = list(campos.values())
    valores.append(id_usuario)

    sql = f"UPDATE `usuarios` SET {colunas} WHERE id_usuario = %s"
    conectar.execute(sql, valores)
    mysql.connection.commit()
    conectar.close()

def buscar_usuario_id(id_usuario: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM usuarios WHERE id_usuario = %s;", (id_usuario,))
    listar = conectar.fetchone()
    conectar.close()

    return listar

def criar_campus(nome):
    conectar = mysql.connection.cursor()
    conectar.execute("INSERT INTO localidade_livro (nome) VALUES (%s)", (nome,)) 
    mysql.connection.commit()
    conectar.close()

def criar_editora(Nome, Telefone, Endereço, Bairro, Cidade, Cep, CNPJ):
    conectar = mysql.connection.cursor()
    conectar.execute("INSERT INTO editora (Nome, Telefone, Endereço, Bairro, Cidade, Cep, CNPJ) VALUES (%s, %s, %s, %s, %s, %s, %s)", (Nome, Telefone, Endereço, Bairro, Cidade, Cep, CNPJ,))
    mysql.connection.commit()
    conectar.close()

def criar_autor(nome, sobrenome):
    conectar = mysql.connection.cursor()
    conectar.execute("INSERT INTO autor (nome, sobrenome) VALUES (%s, %s)", (nome, sobrenome,)) 
    mysql.connection.commit()
    conectar.close()

def criar_genero(genero):
    conectar = mysql.connection.cursor()
    conectar.execute("INSERT INTO genero (genero) VALUES (%s)", (genero,)) 
    mysql.connection.commit()
    conectar.close()

def buscar_editora():
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT * FROM editora")
    row = conectar.fetchall()
    conectar.close()
    return row

def criar_livro(titulo, isbn, id_editora, publicacao, descricao, genero_id, setor, estante, id_campus, autor_id):
    try:
        with mysql.connection.cursor() as conectar:
            conectar.execute(
                "INSERT INTO livro (titulo, ISBN, id_editora, data_publicacao, data_entrada, descricao) "
                "VALUES (%s, %s, %s, %s, CURDATE(), %s)",
                (titulo, isbn, id_editora, publicacao, descricao),
            )
            id_livro = conectar.lastrowid

            conectar.execute("INSERT INTO livro_genero (id_livro, id_genero) VALUES (%s, %s)", (id_livro, genero_id))
            conectar.execute("INSERT INTO livro_autor (id_livro, id_autor) VALUES (%s, %s)", (id_livro, autor_id))
            conectar.execute("INSERT INTO posicao_livro (setor, estante, id_campus, id_livro) VALUES (%s, %s, %s, %s)", (setor, estante, id_campus, id_livro),)
            mysql.connection.commit()
    except Exception: # Isso aqui cancela qual quer erro que de para que não envie informações picotadas
            mysql.connection.rollback()
            raise

def buscar_livro_new(identificador: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT l.id_livro, l.titulo, l.ISBN, DATE_FORMAT(l.data_publicacao,'%%d/%%m/%%Y') AS data_publicacao, e.Nome AS editora, IFNULL(GROUP_CONCAT(DISTINCT CONCAT(a.nome,' ',a.sobrenome) ORDER BY a.sobrenome SEPARATOR ', '),'—') AS autores, IFNULL(GROUP_CONCAT(DISTINCT g.genero ORDER BY g.genero SEPARATOR ', '),'—') AS generos, COUNT(DISTINCT ex.numero_exemplar) AS qtd_exemplares, IFNULL(GROUP_CONCAT(DISTINCT ex.etiqueta ORDER BY ex.numero_exemplar SEPARATOR ', '),'—') AS etiquetas, IFNULL(pl.setor,'—') AS setor, IFNULL(pl.estante,'—') AS estante, IFNULL(loc.nome,'—') AS campus FROM livro l JOIN editora e ON l.id_editora = e.id_editora LEFT JOIN livro_autor la ON l.id_livro = la.id_livro LEFT JOIN autor a ON la.id_autor = a.id_autor LEFT JOIN livro_genero lg ON l.id_livro = lg.id_livro LEFT JOIN genero g ON lg.id_genero = g.id_genero LEFT JOIN exemplares ex ON l.id_livro = ex.id_livro LEFT JOIN posicao_livro pl ON l.id_livro = pl.id_livro LEFT JOIN localidade_livro loc ON pl.id_campus = loc.id_campus WHERE l.id_livro = %s GROUP BY l.id_livro, l.titulo, l.ISBN, data_publicacao, editora, setor, estante, campus;",(identificador,))
    livro = conectar.fetchone()
    conectar.close()
    if livro and livro.get("ISBN"):
        livro["ISBN"] = formatar_isbn(livro["ISBN"])
    return livro
def buscar_exemplares_idlivro(identificador: int):
    conectar = mysql.connection.cursor()
    conectar.execute("SELECT numero_patrimonio, codigo_barras, numero_exemplar, status FROM exemplares WHERE id_livro = %s ORDER BY numero_exemplar;", (identificador,))
    exemplar = conectar.fetchall()
    conectar.close()
    return exemplar