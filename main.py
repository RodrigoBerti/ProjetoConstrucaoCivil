from urllib import request

from lerImagens import *
import requests.utils
from flask import render_template, Flask, request, redirect, session, flash
import mysql.connector as connect, mysql

config = {
    'host':'localhost',
    'user':'root',
    'password':'masterkey',
    'database':'Teste',
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
    material = get_material()
    return render_template("homepage.html", material=material, materiais=materiais, username=username)

#Função para fazer o login
@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST' and request.form['username'] != '':
        session['username'] = request.form['username']
        session['senha'] = request.form['senha']
        return redirect('/')
    return render_template("login.html")
@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect("/")
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


if __name__ == "__main__":
    caminho_da_imagem = 'Design-sem-nome.png'
    imagem = ler_imagem(caminho_da_imagem)
    imagem_processada = preprocessar_imagem(imagem)
    texto_extraido = extrair_informacoes(imagem_processada)
    informacoes = analisar_informacoes(texto_extraido)
    app.run(host='localhost', debug=True)
