from urllib import request

from lerImagens import *
import requests.utils
from flask import render_template, Flask, request, redirect
import mysql.connector as connect, mysql

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='masterkey',
    database='teste',
)

app = Flask(__name__)

materiais = []
# criando pagina
@app.route("/")
def homepage():
    material = get_material()
    return render_template("homepage.html", material=material, materiais=materiais)


@app.route("/login")
def login():
    return render_template('login.html')


def get_material():
    cursor = mydb.cursor()
    cursor.execute('select material.descrição from material')
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
