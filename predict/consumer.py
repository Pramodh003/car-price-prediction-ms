import pika
from fastapi import Depends
from sqlalchemy.orm import Session
from predict.database import get_db
import numpy as np
from sklearn import preprocessing
import pickle
from predict import models
from dotenv import load_dotenv
load_dotenv(".env")
import os
RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT'))
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
label_encoder = preprocessing.LabelEncoder()


predict_model = pickle.load(open('model.pkl','rb'))
    
def process_vehicle_id(vehicle_id: int, db: Session):
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if not vehicle:
        return {"error": "Vehicle not found"}
    print("Fetched vehicle data:", vehicle)
    data_dict = {column.name: getattr(vehicle, column.name) for column in models.Vehicle.__table__.columns}
    categorical_features = ["CarName", "fueltype", "aspiration", "carbody", "drivewheel", "enginelocation", "enginetype", "fuelsystem"]
    numerical_features = ["symboling", "doornumber", "wheelbase", "carlength", "carwidth", "carheight", "curbweight", "cylindernumber", "enginesize", "boreratio", "stroke", "compressionratio", "horsepower", "peakrpm", "citympg", "highwaympg"]
    encoded_feature = []
    for feature in categorical_features:
        encoded = label_encoder.fit_transform([data_dict[feature]])
        encoded_feature.append(encoded[0])
    all_features = encoded_feature + [data_dict[feature] for feature in numerical_features] + [0]
    features = np.array(all_features).reshape(1, -1)
    predicted_price = predict_model.predict(features)
    vehicle.price = float(predicted_price[0])
    db.commit()
    return {"Price_of_car": float(predicted_price[0])}


def callback(ch, method, properties, body):
    vehicle_id = int(body.decode())
    db = next(get_db()) 
    try:
        result = process_vehicle_id(vehicle_id, db)
        print(result)
    finally:
        db.close()
    
def main():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection_parameters = pika.ConnectionParameters(host=RABBITMQ_HOST,port=RABBITMQ_PORT,credentials=credentials)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare(queue='vehicle_queue')
    channel.basic_consume(queue='vehicle_queue', on_message_callback=callback, auto_ack=True)
    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()
    
if __name__ == "__main__":
    main()