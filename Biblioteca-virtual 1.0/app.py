from flask import Flask, render_template, request, redirect, url_for, session, flash
import time
from werkzeug.security import generate_password_hash
from datetime import datetime
import random
import bd

# Retornar_x eu uso para buscar informações para usar em outra função que realmente vai buscar a informação que eu preciso
# Buscar_x eu uso para enviar a informação que eu vou buscar de fato no banco e usar

app = Flask(__name__)
app.secret_key = str(random.randint(0, 10))

bd.init_app(app)

# Rota para pagina inicial
@app.route("/home", methods=["GET", "POST"])
def home():
    livro = bd.buscar_livro_nome()
    return render_template("rotas/principais/home.html", show_navbar=True, livro=livro)

# Rota para pagina inicial
@app.route("/buscaremprestimo", methods=["GET", "POST"])
def buscaremprestimo():
    emprestimo = None
    titulos = bd.buscar_livro_nome()
    if request.method == "POST":
        id_emprestimo = (request.form.get("emprestimo_id") or "").strip()
        livro = (request.form.get("livro_escolhido") or "").strip()
        id_usuario = (request.form.get("id_usuario") or "").strip()
        if id_emprestimo:
            emprestimo = bd.buscar_emprestimo(id_emprestimo)
        elif livro:
            emprestimo = bd.buscar_emprestimo_por_livro(livro)
        elif id_usuario:
            emprestimo = bd.buscar_emprestimo_por_usuario(id_usuario)
    return render_template("rotas/principais/buscaremprestimo.html", show_navbar=True, emprestimo=emprestimo, titulos=titulos)

# Rota para pagina inicial
@app.route("/emprestimo", methods=["GET", "POST"])
def emprestimo():
    livro = bd.buscar_todos_livros()
    usuario = bd.buscar_todos_usuario()
    exemplar = bd.buscar_todos_exemplares()
    emprestimo = bd.buscar_todos_emprestimos()
    livroemprestado = bd.buscar_todos_livrosemprestados()
    return render_template("rotas/principais/emprestimo.html", show_navbar=True,  emprestimo=emprestimo, livro=livro, livroemprestado=livroemprestado, usuario=usuario, exemplar=exemplar)

@app.route("/cadastrogenero", methods=["GET", "POST"])
def cadastro_genero():
    genero = bd.buscar_todos_generos()
    if request.method == "POST":
        genero_c = request.form.get("genero")

        bd.criar_genero(genero_c)
        return redirect(url_for('cadastro_genero'))
    return render_template("rotas/cadastro/cadastrar_generos.html", show_navbar=True, genero=genero)

@app.route("/cadastroeditora", methods=["GET", "POST"])
def cadastro_editora():
    if request.method == "POST":
        Nome = request.form.get("nome")
        Telefone = request.form.get("telefone")
        Endereço = request.form.get("endereco")
        Bairro = request.form.get("bairro")
        Cidade= request.form.get("cidade")
        Cep = request.form.get("cep")
        cnpj = request.form.get("cnpj")

        bd.criar_editora(Nome, Telefone, Endereço, Bairro, Cidade, Cep, cnpj)
    return render_template("rotas/cadastro/cadastro_editora.html", show_navbar=True)

@app.route("/cadastroautor", methods=["GET", "POST"])
def cadastro_autor():
    autor = bd.buscar_todos_autores()
    if request.method == "POST":
        nome = request.form.get("nome")
        sobrenome = request.form.get("sobrenome")
        bd.criar_autor(nome, sobrenome)

    return render_template("rotas/cadastro/cadastrar_autores.html", show_navbar=True, autor=autor)
# Rota para pagina inicial

@app.route("/cadastrolocalidade", methods=["GET", "POST"])
def cadastro_localidade():
    titulos = bd.buscar_livro_nome()
    campus_lista = bd.buscar_campus()
    campus_escolhido = request.form.get("campus_escolhido") 
    livro_escolhido = request.form.get("livro_escolhido")
    setor = request.form.get("setor")
    estante = request.form.get("estante")

    if request.method == "POST":
        bd.criar_posicaolivro(setor, estante, campus_escolhido, livro_escolhido)
        campus = request.form.get("campus")
        if campus:
            bd.criar_campus(campus)
        
    return render_template("rotas/cadastro/cadastro_localidade.html", show_navbar=True, campus_l=campus_lista, titulos=titulos)

# Rota para cadastro de livros
# Verificar se não é ideal trocar para um nome melhor 
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():        
    return render_template("rotas/cadastro/cadastro.html", show_navbar=True)

@app.route("/cadastrolivros", methods=["GET", "POST"])
def cadastrolivros():
    todos_generos = bd.buscar_todos_generos()
    todos_autores = bd.buscar_todos_autores()
    todos_editoras = bd.buscar_editora()
    campus_lista = bd.buscar_campus()
    if request.method == "POST":
        titulo = request.form.get("titulo")
        isbn = request.form.get("isbn")
        id_editora = request.form.get("editora_escolhido")
        publicacao = request.form.get("data_publicacao")
        descricao = request.form.get("descricao")
        genero_id = request.form.get("genero_escolhido")
        setor = request.form.get("setor")
        estante = request.form.get("estante")
        id_campus = request.form.get("campus_escolhido")
        autor_id = request.form.get("autor_escolhido")

        bd.criar_livro(titulo, isbn, id_editora, publicacao, descricao, genero_id, setor, estante, id_campus, autor_id)
    return render_template("rotas/cadastro/cadastrolivros.html", show_navbar=True, autores=todos_autores, generos=todos_generos, editora=todos_editoras, campus=campus_lista)

# Rota para buscar as informações de livros
@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    titulo = bd.buscar_livro_nome()
    livro = None
    exemplar = None
    if request.method == "POST":
        idlivro = request.form.get("idlivro")
        titulo_escolhido = request.form.get("titulo_escolhido")
        isbn = request.form.get("isbn")
        if idlivro:
            livro = bd.buscar_livro_new(idlivro)
            exemplar = bd.buscar_exemplares_idlivro(idlivro)
        elif titulo_escolhido:
            livro = bd.buscar_livro_new(titulo_escolhido)
            exemplar = bd.buscar_exemplares_idlivro(titulo_escolhido)
        elif isbn:
            livro = bd.buscar_livro_isbn(isbn)
    return render_template("rotas/principais/buscar.html", show_navbar=True, livro=livro, titulo=titulo, exemplar=exemplar)


# Rota para cadastrar o usuario
# nome, data_nascimento, email, cpf, telefone, senha, nivel_acesso
@app.route("/cadastrar_usuario", methods=["GET", "POST"])
def cadastrar_usuario():
    confirma = None
    if request.method == "POST":
        nome_info = request.form.get("Nome")
        data_nascimento_info = request.form.get("Data_nascimento")
        email_info = request.form.get("Email")
        cpf_info = request.form.get("CPF")
        telefone_info = request.form.get("Telefone")
        senha_info = request.form.get("Senha")
        c_senha_info = request.form.get("c_Senha")
        lvl_acess_info = request.form.get("lvl_acess")
        validar_confirma = request.form.get("confirmacao")
        validar_negado = request.form.get("negado")
        verificar = bd.verificar_usuario(email_info,cpf_info)
        
        if validar_confirma == "confirmar":
            if not verificar:
                if senha_info == c_senha_info:
                    bd.criar_usuario(nome_info, data_nascimento_info, email_info, cpf_info, telefone_info, senha_info, lvl_acess_info)
                    confirma = True
                else:
                    confirma = False
        elif validar_negado == "negar":
            confirma = False
            
    return render_template("rotas/cadastro/cadastrar_usuario.html", show_navbar=True, msg=confirma)

# Pagina para efetuar o login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario_id = request.form.get("usuario")
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        if bd.verificar_usuario_id(usuario_id, senha):
            user = bd.verificar_usuario_id(usuario_id, senha)
            if user:
                # Essa parte aqui foi feita para guardar os usuarios    
                dn = user.get("data_nascimento")
                dn_fmt = dn.strftime("%d/%m/%Y") if dn else None

                session["user"] = {
                    "id": user.get("id_usuario"),
                    "nome": user.get("nome"),
                    "data_nascimento": dn_fmt,
                    "email": user.get("email"),
                    "cpf": user.get("cpf"),
                    "telefone": user.get("telefone"),
                    "nivel_acesso": user.get("nivel_acesso")
                }
                return redirect(url_for('home'))
            elif not session.get("user") or not bd.verificar_usuario_id(usuario_id, senha):
                erro = True
                return render_template("rotas/principais/index.html", erro=erro, msg="Usuário ou senha inválidos.")
            
        if bd.verificar_usuario_nome(usuario, senha):
            user = bd.verificar_usuario_nome(usuario, senha)
            if user:
                # Essa parte aqui foi feita para guardar os usuarios    
                dn = user.get("data_nascimento")
                dn_fmt = dn.strftime("%d/%m/%Y") if dn else None

                session["user"] = {
                    "id": user.get("id_usuario"),
                    "nome": user.get("nome"),
                    "data_nascimento": dn_fmt,
                    "email": user.get("email"),
                    "cpf": user.get("cpf"),
                    "telefone": user.get("telefone"),
                    "nivel_acesso": user.get("nivel_acesso")
                }
                return redirect(url_for('home'))
        elif not session.get("user") or not bd.verificar_usuario_nome(usuario_id, senha):
            erro = True
            return render_template("rotas/principais/index.html", erro=erro, msg="Usuário ou senha inválidos")
    return render_template("rotas/principais/index.html")

@app.route("/usuario", methods=["GET", "POST"])
def usuario():
    if request.method == "POST":
        nome = (request.form.get("nome") or "").strip()
        email = (request.form.get("email") or "").strip()
        telefone = (request.form.get("telefone") or "").strip()
        cpf = (request.form.get("cpf") or "").strip()
        data_nascimento = (request.form.get("data_nascimento") or "").strip()
        nivel_acesso = (request.form.get("nivel_acesso") or "").strip()
        id_usuario = session.get("user", {}).get("id")

        if id_usuario:
            campos = {}
            if nome: campos["nome"] = nome
            if email: campos["email"] = email
            if telefone: campos["telefone"] = telefone
            if cpf: campos["cpf"] = cpf
            if data_nascimento: campos["data_nascimento"] = data_nascimento
            if nivel_acesso: campos["nivel_acesso"] = nivel_acesso

            if campos:
                bd.atualizar_usuario(id_usuario, **campos)

            user = bd.buscar_usuario_id(id_usuario)
            if user:
                dn = user.get("data_nascimento")
                dn_fmt = dn.strftime("%d/%m/%Y") if dn else None
                session["user"] = {
                    "id": user.get("id_usuario"),
                    "nome": user.get("nome"),
                    "data_nascimento": dn_fmt,
                    "email": user.get("email"),
                    "cpf": user.get("cpf"),
                    "telefone": user.get("telefone"),
                    "nivel_acesso": user.get("nivel_acesso")
                    }

    return render_template("rotas/principais/usuario.html", show_navbar=True)

# Deslogar o usuario
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for('login'))

def visibilidade_nivel(*levels: int) -> bool:
    return session.get("nivel_acesso") in levels

# Essa função injeta em todas as paginas as informações que contem nela
@app.context_processor
def inject_user():
    return dict(usuario=session.get("user"), nivel=session.get("user", {}).get("nivel_acesso"), visibilidade_nivel=visibilidade_nivel)

# Até agora não entendo como funciona mas é importante para o codigo
if __name__ == "__main__":
    app.run(debug=True)