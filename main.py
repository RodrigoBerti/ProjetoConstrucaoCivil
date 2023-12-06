from urllib import request

from lerImagens import *
import requests.utils
from flask import render_template, Flask, request, redirect, session, flash
import mysql.connector as connect, mysql

config = {
    'host':'localhost',
    'user':'root',
    'password':'masterkey',
    'database':'teste',
}
app = Flask(__name__)
app.config['SECRET_KEY'] = "1234"

# faz a connexão com o banco de dados
def conectorBD():
    try:
        conn = mysql.connector.connect(**config)
        print("Banco de dados conectado com sucesso")
    except:
        print("Erro com a conexão do banco de dados")
    else:
        return conn

#desconecta do banco de dados
def desconectandoBD(conn):
    return conn.close()

materiais = []
# criando pagina
@app.route("/")
def homepage():
    username = None
    senha = None
    if 'username' in session:
        username = session['username']
    return render_template("homepage.html",username=username)

@app.route("/orcamento")    # adiciona os materiais no orcamento
def ormamento():
    material = get_material()
    return render_template("orcamento.html", material=material, materiais=materiais)

#Função para fazer o login
@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST' and request.form['username'] != '':
        mybd = conectorBD()
        cursor = mybd.cursor()
        cursor.execute(f"select usuario.codusuario from usuario where usuario.email='{request.form['username']}' and usuario.senha={request.form['senha']}")

        if not cursor.fetchall():
            flash('Username ou senha incorretos ou usuário não encontrado')
            return render_template("login.html")

        session['codusuario'] = cursor.fetchall()
        cursor.execute('select material.descricao from material')
        return redirect('/index')
    return render_template("login.html")
@app.route('/logout')
def logout():
   session.pop('codusuario', None)
   return redirect("/")

#Rota para o link de cadastro
@app.route("/cadastro")
def cadastro():
    return render_template('cadastro.html')
#Rota para inserir as informações cadastrais no banco de dados
@app.route("/cadastrar", methods=['POST','GET'])
def cadastrar():
    nome = request.form.get('nome')
    sobrenome = request.form.get('sobrenome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    if verificaEmail(email) != True:
        sql = 'INSERT INTO usuario (nome,login,senha,premium) VALUES (%s,%s,%s,%s)'
        val = (nome,email,senha,0)
        mybd = conectorBD()
        cursor = mybd.cursor()
        cursor.execute(sql, val)
        mybd.commit()
        return render_template("login.html")
    else:
        flash("Email já cadastrado")
        return redirect("cadastro")

def get_material():
    mybd = conectorBD()
    cursor = mybd.cursor()
    cursor.execute('select material.descricao from material')
    meus_materiais = cursor.fetchall()
    return meus_materiais

@app.route("/adicionar",methods=["POST"])
def adicionar_material():
    material= request.form.get('materiais')
    quantidade = request.form.get('quantidade')
    materiais.append(
        {'material':material, 'quantidade':quantidade}
    )
    return redirect("/")

@app.route('/atualizar/<int:index>', methods=['POST'])
def atualizar(index):
    quantidade = request.form.get('quantidade')
    materiais[index]['quantidade'] = quantidade
    return redirect('/')

@app.route('/excluir/<int:index>')
def excluir(index):
    materiais.pop(index)
    return redirect('/')

def verificaEmail(email):
    mybd = conectorBD()
    cursor = mybd.cursor()
    comando_sql = f"select usuario.login from usuario where usuario.email = '{email}' "
    cursor.execute(comando_sql)
    if not cursor.fetchone():
        return True
    else:
        return False


if __name__ == "__main__":
    caminho_da_imagem = 'Design-sem-nome.png'
    imagem = ler_imagem(caminho_da_imagem)
    imagem_processada = preprocessar_imagem(imagem)
    texto_extraido = extrair_informacoes(imagem_processada)
    informacoes = analisar_informacoes(texto_extraido)
    app.run(host='localhost', debug=True)