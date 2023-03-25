import os

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

import tensorflow as tf
from tensorflow import keras

#============================================================================

def meal(data):
    #1,2,3,not selected
    a=[0,0,0,0]
    if data=='Meal Plan 1':
        a[0]=1
    if data=='Meal Plan 2':
        a[1]=1
    if data=='Meal Plan 3':
        a[2]=1
    if data=='Not Selected':
        a[3]=1
    return a
def room(data):
    a=[0,0,0,0,0,0,0]
    if data=='Room_Type 1':
        a[0]=1
    if data=='Room_Type 2':
        a[1]=1
    if data=='Room_Type 3':
        a[2]=1
    if data=='Room_Type 4':
        a[3]=1
    if data=='Room_Type 5':
        a[4]=1
    if data=='Room_Type 6':
        a[5]=1
    if data=='Room_Type 7':
        a[6]=1
    return a



def market(data):
    a=[0,0,0,0,0]
    if data=='Aviation':
        a[0]=1
    if data=='Complementary':
        a[1]=1
    if data=='Corporate':
        a[2]=1
    if data=='Offline':
        a[3]=1
    if data=='Online':
        a[4]=1
    return a



def booking(data):
    a=[0,0]
    if data=='Canceled':
        a[0]=1
    if data=='Not_Canceled':
        a[1]=1
    return a



def year(data):
    a=[0,0]
    if data==2017:
        a[0]=1
    if data==2018:
        a[1]=1
    return a



def month(data):
    a=[0]*12
    a[data-1]=1
    return a


def date(data):
    a=[0]*31
    a[data-1]=1
    return a

def min_max_scale(data):
    data_min = 0
    data_max = 443
    # Calcula a escala Min-Max
    scaled_data = (data - data_min) / (data_max - data_min)
    return scaled_data

def find_max_index(vector):
    # Encontra o índice do maior valor usando o método index()
    max_index = vector.index(max(vector))

    return max_index

def predictFunc(inputs):
    new_model = tf.keras.models.load_model('modelo.h5')
    predictions = new_model.predict([inputs])
    max_index=find_max_index(list(predictions[0]))
    return max_index

def FormatInput(data):
   no_of_adults =  data['no_of_adults']
   no_of_children = data['no_of_children']
   no_of_weekend_night = data['no_of_weekend_night']
   no_of_week_nights=data['no_of_week_nights']
   required_car_parking_space=data['required_car_parking_space']
   lead_time=min_max_scale(data['lead_time'])
   repeated_guest=data['repeated_guest']
   no_of_previous_cancellations=data["no_of_previous_cancellations"]
   no_of_previous_bookings_not_canceled=min_max_scale(data['no_of_previous_bookings_not_canceled'])
   no_of_special_requests=data['no_of_special_requests']

   #valores categoricos
   type_of_meal_plan=meal(data['type_of_meal_plan'])
   room_type_reserved=room(data['room_type_reserved'])
   market_segment_type=market(data['market_segment_type'])
   booking_status=booking(data['booking_status'])
   arrival_year=year(data['arrival_year'])
   arrival_month=month(int(data['arrival_month']))
   arrival_date=date(int(data['arrival_date']))

   predict=[no_of_adults,no_of_children,no_of_weekend_night,no_of_week_nights,required_car_parking_space,lead_time,repeated_guest,no_of_previous_cancellations,no_of_previous_bookings_not_canceled,no_of_special_requests]
   predict=predict+type_of_meal_plan+room_type_reserved+market_segment_type+booking_status+arrival_year+arrival_month+arrival_date
   return predict

@app.route('/api/v1/predicts', methods=['POST'])
def create_user():
    data = request.get_json()
    dados_entrada=FormatInput(data)
    val_predict=predictFunc(dados_entrada)
    response={'result':val_predict}
    return jsonify(response)
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/process_form", methods=['POST'])
def process_form():
    data = {
        "no_of_adults": int(request.form.get("adult_number")),
        "no_of_children": int(request.form.get("child_number")),
        "no_of_weekend_night": int(request.form.get("weekend_nights")),
        "no_of_week_nights": int(request.form.get("weekday_nights")),
        "required_car_parking_space": int(request.form.get("parking_space")),
        "lead_time": int(request.form.get("waiting_time")),
        "repeated_guest": int(request.form.get("repeated_booking")),
        "no_of_previous_cancellations": int(request.form.get("canceled_bookings")),
        "no_of_previous_bookings_not_canceled": int(request.form.get("not_canceled_bookings")),
        "no_of_special_requests": int(request.form.get("special_requests")),
        
        "type_of_meal_plan": request.form.get("meal-plan"),
        "room_type_reserved": request.form.get("room_type_reserved"),
        "market_segment_type": request.form.get("market_segment_type"),
        "booking_status" :request.form.get('booking-status'),
        "arrival_year" :int(request.form.get('arrival-year')),
        "arrival_month" : int(request.form.get('arrival-month')),
        "arrival_date" : int(request.form.get('arrival-date'))
    }
    response = requests.post("http://Appflask-env.eba-7egh3jnn.us-east-1.elasticbeanstalk.com/api/v1/predicts", json=data)
    if response.status_code == 200:
        dados = response.json()
        return dados
    else:
        return 'aplicação com erro'

if __name__ == '__main__':
    app.run()