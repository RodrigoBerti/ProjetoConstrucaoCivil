from urllib import request

from lerImagens import *
import requests.utils
from flask import render_template, Flask, request
import mysql.connector as connect, mysql
#from mysql.connector import connect, errorcode as mysql

config = {
    'host':'localhost',
    'user':'root',
    'password':'masterkey',
    'database':'Teste',
}

app = Flask(__name__)


# criando pagina
@app.route("/")
def homepage():
    material = get_material()
    return render_template("homepage.html", material=material)


@app.route("/login")
def login():
    return render_template('login.html')


def get_material():
    mybd = conectorBD()
    cursor = mybd.cursor()
    cursor.execute('select material.descrição from material')
    meus_materiais = cursor.fetchall()
    return meus_materiais

@app.route("/adicionar",methods=["POST"])
def adicionar_material():
    material= request.form['materiais']
    quantidade = request.form['quantidade']
    return render_template("homepage.html",material_adicionado=material,quantidade=quantidade)

def conectorBD():
    try:
        conn = mysql.connector.connect(**config)
        print("Banco de dados conectado com sucesso")
    except:
        print("Erro com a conexão do banco de dados")
    else:
        return conn

def desconectandoBD(conn):
    return conn.close()
if __name__ == "__main__":
    caminho_da_imagem = 'Design-sem-nome.png'
    imagem = ler_imagem(caminho_da_imagem)
    imagem_processada = preprocessar_imagem(imagem)
    texto_extraido = extrair_informacoes(imagem_processada)
    informacoes = analisar_informacoes(texto_extraido)
    app.run(host='localhost', debug=True)
