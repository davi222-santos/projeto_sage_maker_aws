# Importação das bibliotecas necessárias do Flask
# request - permite ler os dados enviados na requisição HTTP
# jsonify - permite retornar dados no formato JSON na resposta HTTP
# Blueprint - permite organizar o código em estruturas reutilizáveis
from flask import Blueprint, jsonify, request
from services import entrance, predict

# Cria um objeto blueprint chamado "bp" com o nome "blueprint_name"
# e o associa ao arquivo atual (__name__)
bp = Blueprint('blueprint_name', __name__)

# Define um endpoint para o blueprint "bp" com a rota "/api/v1/predicts"
# e permite apenas o acesso por método POST a ele
@bp.route('/api/v1/predicts', methods=['POST'])

#Função que cria um novo usuário.
#Este endpoint é acessível apenas via método POST e espera receber
#dados no formato JSON como corpo da solicitação. 
def create_user():
    
    # Recupera os dados no formato JSON da solicitação
    data = request.get_json()
    dados_entrada=entrance.FormatInput(data)
    val_predict=predict.predictFunc(dados_entrada)
    response={'result':val_predict}
    # Retorna os dados em formato JSON como resposta
    return jsonify(response)


