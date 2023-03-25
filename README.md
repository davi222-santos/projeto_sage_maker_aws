# Avaliação Sprint 5 - Programa de Bolsas Compass UOL / AWS e IFCE

[![N|Solid](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/LogoCompasso-positivo.png/440px-LogoCompasso-positivo.png)](https://compass.uol/pt/home/)


## Objetivos

1 - Treinar o modelo utilizando Sage Maker, e fazer o salvamento do modelo para o S3.

2 - Criar um ambiente Docker no AWS Elastic Beanstalk.

3 - Desenvolver um serviço em python (API), utilizando o framework http Flask, que deve carregar o modelo treinado do S3 e expor um endpoint para realizar a inferência.

## Ferramentas / plataformas utilizadas

* Visual Studio Code (VS Code)
* Github
* Amazon Web Services (AWS)
* Python

## Especificações

Segue abaixo, a estrutura do projeto, com divisão de responsabilidades em arquivos/pastas distintos, visando melhor manutenibilidade e escalabilidade do código:

![img01](https://user-images.githubusercontent.com/80013300/215467749-a4c2ba6c-2419-41da-baa9-7a3f08a19871.png)

Dentro da **src** temos quatro pastas onde dividimos as tarefas executadas por nossa aplicação, visando uma melhor organização:

* **resources:**Arquivos necessários para o funcionamento do projeto que não são código fonte.
* **routes:** Pesponsável por armazenar com aquivos contendo as rotas da aplicação.
* **services:**Provê serviços adjacentes, porém necessarios a aplicação.
* **utils:**Funções e utilitários para as aplicações

## Treinamento de dados:
A principal proposta da atividade é preparar o conjunto de dados **Hotel Reservations Dataset**, que contém informações sobre reservas de hotel, e treina-lo de modo que apartir de uma entrada o sistema consiga prever e retornar a determinada faixa de preço:
* **0 - Para valores até 85 euros**
* **1 - Para valores entre 85 e 115 euros**
* **2 - Para valores acima de 115 euros**
## 1.1 Sobre o dataset:
O dataset  **[Hotel Reservations Dataset][d1]** cotém cerca de 19 colunas e possui cerca de **36275** dados.
Em suas colunas temos:
* **Booking_ID** : identificador único de cada reserva
* **no_of_adults** : número de adultos
* **no_of_children** : Número de filhos
* **no_of_weekend_nights** : Número de noites de fim de semana (sábado ou domingo) que o hóspede ficou ou reservou para ficar no hotel
* **no_of_week_nights** : Número de noites da semana (segunda a sexta) que o hóspede ficou ou reservou para ficar no hotel
* **type_of_meal_plan** : Tipo de plano de refeição reservado pelo cliente:
* **required_car_parking_space** : O cliente precisa de uma vaga de estacionamento? (0 - Não, 1- Sim)
* **room_type_reried** : Tipo de quarto reservado pelo cliente. Os valores são cifrados (codificados) pela INN Hotels.
* **lead_time** : Número de dias entre a data da reserva e a data de chegada
* **arrival_year** : Ano da data de chegada
* **arrival_month** : Mês da data de chegada
* **arrival_date** : Data do mês
* **market_segment_type** : Designação do segmento de mercado.
* **repeat_guest** : O cliente é um convidado repetido? (0 - Não, 1- Sim)
* **no_of_previous_cancellations** : Número de reservas anteriores que foram canceladas pelo cliente antes da reserva atual
* **no_of_previous_bookings_not_canceled** : Número de reservas anteriores não canceladas pelo cliente antes da reserva atual
* **avg_price_per_room** : Preço médio por dia da reserva; os preços dos quartos são dinâmicos. (em euros)
* **no_of_special_requests** : Número total de solicitações especiais feitas pelo cliente (por exemplo, andar alto, vista do quarto, etc)
* **booking_status** : Flag indicando se a reserva foi cancelada ou não.

Para mais informações sobre os dados consulte a [documentação][d1]
## 1.2 Tratamento dos dados
Antes de treinar um conjunto de dados é importante tratá-los, um bom pré-processamento de dados ajuda o modelo de treinamento a ganhar mais performace e acertos.
O treinamento foi feito usando o Google colab e a biblioteca Pandas do python (notebook disponivel em **src/services/pre-processamento.ipynb**).

O primeiro passo do processo foi deletar a coluna **Booking_ID** já que ela não oferece nenhuma informação relevante ao conjunto, com o Pandas isso pode ser feito da seguinte maneira:
``` del df["Booking_ID"] ```
O próximo passo a ser feito é converter os dados que contém informações qualitativas em informações quantitativas, pois a rede neural só reconhece numeros como dados de entrada.
A biblioteca Pandas provê a função **get_dummies** para realizar a codificação dos dados, assim como no código abaixo:
```
colunas_dummies = ['type_of_meal_plan', 'room_type_reserved', 'market_segment_type','booking_status','arrival_year','arrival_month',"arrival_date"]
df = pd.get_dummies(df, prefix = colunas_dummies, columns = colunas_dummies)
```
**Obs**. As colunas **arrival_year**, **arrival_month** e **arrival_date** apesar de serem dados numéricos foram classificados como classes, escolha baseada em testes de precisão com o modelo.

Outro cuidado que tem que se ter ao analizar um conjunto de dados é observar se todos os valores estão na mesma escala, pois se os valores tiverem uma discrepância muito grande acaba prejudicando a performace da rede.
Esse processo se chama normalização, ele coloca todos os dados em um determinado intervalo, essa técnica foi aplica em duas principais colunas: **lead_time** e **no_of_previous_bookings_not_canceled** usando a função da biblioteca **sklearn**:
```
from sklearn.preprocessing import minmax_scale
df['lead_time'] = minmax_scale(df['lead_time'])
df['no_of_previous_bookings_not_canceled'] = minmax_scale(df['no_of_previous_bookings_not_canceled'])
```
Como a ideia principal da aplicação é prever faixa de valores que serão gastos por reserva precisamos codificar a coluna alvo **avg_price_per_room** em uma cova coluna **label_avg_price_per_room**, para isso criamos uma função que codifica os valores, passaremos por todas as linhas da tabela de preço, colocaremos esses valores na nova tabela de preço e apagaremos  tebela de preço antiga.
```
def classifica_valores(valor):
    return np.where(valor <= 85, 0,
                    np.where(np.logical_and(valor > 85, valor <= 115), 1, 2))
#Criação da coluna "label_avg_price_per_room" e atribuição da mesma a codificação da coluna "avg_price_per_room"
df["label_avg_price_per_room"]=df["avg_price_per_room"].apply(classifica_valores)

#Apagando a coluna "avg_price_per_room"
del df["avg_price_per_room"]
```
Agora que temos os dados pré processados podemos realizar o heatmap, ele é uma representação visual que exibe dados em forma de uma matriz onde os valores são representados por cores.
![Image 2023-01-31 at 15 25 40](https://user-images.githubusercontent.com/106123150/215868365-9a71ca46-651c-4340-8c44-5f7ec131e3d1.jpeg)

## 2.0 Treinamendo de dados

Para o treinamento foi utilizado a biblioteca TensorFlow juntamente com o serviço de aprendizado da AWS Sagemaker.

Para isso foi criando um ambiente dentro do [sagemaker][d2], ao criar esse ambiente foi gerado um bucket no S3,um serviço oferecido pela Amazon Web Services que fornece armazenamento de objetos por meio de uma interface de serviço da web, por meio dele que será lido o dataset e salvo o modelo de aprendizado depois de treinado.

Para a comunicação entre o sagemaker e o bucket s3 foi utilizado a biblioteca [boto3][d3] um SDK python que facilita a integração da aplicação, biblioteca ou script Python aos serviços da AWS.

Ao criar um documento do tipo TensorFlor (biblioteca para a criação de modelo de rede neurais), foi feita a importação do arquivo de dataset treinado no passo anterior, atraves do seguinte comando:
```
import boto3
s3 = boto3.client('s3')
bucket_name = 'bucketgrupo2'
response = s3.get_object(Bucket='bucketgrupo2', Key='dataset_processado.csv')
data = response['Body'].read()

#O arquivo binário é lido e transformado em sua extensão original CSV e após isso em um dataframe do pandas
df = pd.read_csv(io.StringIO(data.decode('utf-8')))
```

Agora que temos acesso ao dataset vamos criar o modelo da seguinte maneira:
```
from tensorflow.keras import datasets, layers, models
from sklearn.model_selection import train_test_split
from tensorflow import keras
from tensorflow.keras.layers import Dropout
from tensorflow.keras.callbacks import ModelCheckpoint


X = df.drop("label_avg_price_per_room", axis=1)
y = df["label_avg_price_per_room"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#y_test = keras.utils.to_categorical(y_test, num_classes=3)
#y_train = keras.utils.to_categorical(y_train, num_classes=3)

model = keras.Sequential()
model.add(layers.Dense(73, input_shape=(X.shape[1],), activation='relu'))
model.add(layers.Dense(37, activation='relu'))
model.add(Dropout(0.3))
model.add(layers.Dense(37, activation='relu'))
model.add(Dropout(0.3))
model.add(layers.Dense(37, activation='relu'))
model.add(keras.layers.Dense(3, activation='softmax'))
```
Essa arquitetura foi feita baseada em testes de acuracia sobre os dados treinados, como o overfiting (excesso de treinamento) foi observdo em grande parte dos testes, optou-se por uma tecnica de regularização chamada Dropout, ela 'mata' alguns neurônios forçando o modelo a criar novos pesos, assim podendo ganhar mais poder de generalização.
As funções de ativação também foram escolhidas empiricamente, sendo testadas a sigmoid e tangente hiperbola na ultima camada.
A compilação e treinamento ocorreu dessa maneira:
```
model.compile(optimizer='adam',
              loss=keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])


history = model.fit(X_train, y_train, epochs=100,batch_size=64,
                    validation_data=(X_test, y_test))

test_loss, test_acc = model.evaluate(X_test, y_test, verbose=2)
print("Test accuracy:", test_acc)
```

Com essa Arquitetura foi possivel obter cerca de 83% de acuracia.
Agora com o modelo treinado vamos usar novamente a biblioteca boto3 para salvar esse modelo no bucket S3.
```
model.save('modelo.h5')
with open('modelo.h5', 'rb') as data:
    s3.upload_fileobj(data, bucket_name, 'modelo.h5')
```
Arquivo encontrado em src/services/tensorflow-hotel-sagemaker.ipynb

#Criação da api
A criação da api usa o micro framework Flask que provê as funcionalidades necessárias.

##Criação da rota
para criar uma rota em flask é simples:
```
from routes.predict_route import bp
from services import predict

app = Flask(__name__)
# Registra o blueprint na aplicação
app.register_blueprint(bp)


if __name__ == '__main__':
    app.run(debug=True)
```
Para um melhor organização estamos utilizandos blueprints, esse blueprint da aplicação está registrado na seguinte rota:
```
from flask import Blueprint, jsonify, request
from services import entrance, predict

bp = Blueprint('blueprint_name', __name__)

@bp.route('/api/v1/predicts', methods=['POST'])

def create_user():
    data = request.get_json()
    dados_entrada=entrance.FormatInput(data)
    val_predict=predict.predictFunc(dados_entrada)
    response={'result':val_predict}
    return jsonify(response)
```
Essa rota recebe os dados json enviados passados pelo usuário através da rota /api/v1/predicts via POST e passa pela função entrance.FormatInput que trata os dados de entrada organizando-os para a entrada da rede neural, e assim é feito a função predict.predicFunc realiza essa predição, ambas bibliotecas disponiveis em src/services.

É criado um json e retornado para o usuário a predição.

:)



[d1]: <https://www.kaggle.com/datasets/ahsan81/hotel-reservations-classification-dataset>
[d2]: <https://aws.amazon.com/pt/pm/sagemaker/?trk=41368dcc-5040-4349-998b-a9c524544f65&sc_channel=ps&s_kwcid=AL!4422!3!532488969022!p!!g!!sagemaker&ef_id=CjwKCAiAleOeBhBdEiwAfgmXfzsNQbF501LiS-tYKM2THKyBn8_EADX3TbnVEeBXuw5cHiYBSyb0vxoCW1wQAvD_BwE:G:s&s_kwcid=AL!4422!3!532488969022!p!!g!!sagemaker>
[d3]: <https://aws.amazon.com/pt/sdk-for-python/>


## Deploy
Para fazer o deploy foi utilizado o Elastic Beanstalk é uma plataforma da Amazon Web Services (AWS) para implantação e gerenciamento de aplicativos web. 

Foi abstraido apenas as informações necessárias para colocar uma aplicação funcional em nuvem, assim foi criada a pasta mini-app, nela contém uma versão simplificada da aplicação.
Desse modo nosso container docker ficaria dessa maneira:
```
FROM  tensorflow/tensorflow:latest

WORKDIR /app

COPY . /app
RUN pip3 install --upgrade pip
RUN pip3 install flask



ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
```
Note que: A imagem usada para o container foi uma imagem que já possui o tensorflow, isso ocorreu pelo fato de em alguns casos o docker não consegue baixar via pip install todas as dependências do tensorflow.

Dentro do Elastic Beanstalk foi criado um ambiente para a nossa aplicação, selecionando um nome e o tipo da plataforma no nosso caso Docker, comprimimos os arquivos da pasta mini-app em .zip e fazemos o upload do código.

Aplicação pronta e disponivel no seguinte link:

http://appflask-env.eba-7egh3jnn.us-east-1.elasticbeanstalk.com/api/v1/predicts

# Extra
Para facilitar a inferencia de dados foi adicionado um Forms na rota raiz que gera o json e envia para a rota predicts.
http://appflask-env.eba-7egh3jnn.us-east-1.elasticbeanstalk.com/
Obs. Ela não possui tratamentos de erro para dados inválidos.

## Autores

* [@herissonhyan](https://github.com/herissonhyan)
* [@Rosemelry](https://github.com/Rosemelry)
* [@davi222-santos](https://github.com/davi222-santos)
* [@Rangelmello](https://github.com/Rangelmello)



