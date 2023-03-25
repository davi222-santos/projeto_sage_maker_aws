
# Importação das bibliotecas necessárias do Flask
# request - permite ler os dados enviados na requisição HTTP
# jsonify - permite retornar dados no formato JSON na resposta HTTP
# Blueprint - permite organizar o código em estruturas reutilizáveis
from flask import Blueprint, Flask, jsonify, request

# Importação do blueprint criado no arquivo "predict_route.py"
# Este arquivo contém as rotas relacionadas à previsão
from routes.predict_route import bp
from services import predict

# Inicialização da aplicação Flask
# O argumento __name__ permite identificar o módulo atual
app = Flask(__name__)
FLASK_APP='app.py'
# Registra o blueprint na aplicação
app.register_blueprint(bp)

# Verifica se o arquivo está sendo executado diretamente
if __name__ == '__main__':
    # Inicia a aplicação com o modo de depuração ativado
    # O modo de depuração permite ver erros detalhados na tela do navegador
 
    app.run()