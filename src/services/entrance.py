from utils.entranceUtils import dummies, functions


def FormatInput(data):
   no_of_adults =  data['no_of_adults']
   no_of_children = data['no_of_children']
   no_of_weekend_night = data['no_of_weekend_night']
   no_of_week_nights=data['no_of_week_nights']
   required_car_parking_space=data['required_car_parking_space']
   lead_time=functions.min_max_scale(data['lead_time'])
   repeated_guest=data['repeated_guest']
   no_of_previous_cancellations=data["no_of_previous_cancellations"]
   no_of_previous_bookings_not_canceled=functions.min_max_scale(data['no_of_previous_bookings_not_canceled'])
   no_of_special_requests=data['no_of_special_requests']

   #valores categoricos
   type_of_meal_plan=dummies.type_of_meal_plan(data['type_of_meal_plan'])
   room_type_reserved=dummies.room_type_reserved(data['room_type_reserved'])
   market_segment_type=dummies.market(data['market_segment_type'])
   booking_status=dummies.booking(data['booking_status'])
   arrival_year=dummies.arrival_year(data['arrival_year'])
   arrival_month=dummies.arrival_month(int(data['arrival_month']))
   arrival_date=dummies.arrival_date(int(data['arrival_date']))

   predict=[no_of_adults,no_of_children,no_of_weekend_night,no_of_week_nights,required_car_parking_space,lead_time,repeated_guest,no_of_previous_cancellations,no_of_previous_bookings_not_canceled,no_of_special_requests]
   predict=predict+type_of_meal_plan+room_type_reserved+market_segment_type+booking_status+arrival_year+arrival_month+arrival_date
   return predict