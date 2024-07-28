import os
import pika
from fastapi import Depends
from sqlalchemy.orm import Session
from predict.database import get_db
import numpy as np
from sklearn import preprocessing
import pickle
from predict import models
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")

RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT'))
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')

label_encoder = preprocessing.LabelEncoder()

# Load the model
predict_model = pickle.load(open('model.pkl', 'rb'))

def process_vehicle_id(vehicle_id: int, db: Session):
    print(f"Processing vehicle ID: {vehicle_id}")
    vehicle = db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()
    if not vehicle:
        print(f"Vehicle ID {vehicle_id} not found")
        return {"error": "Vehicle not found"}

    print(f"Fetched vehicle data for ID {vehicle_id}: {vehicle}")
    data_dict = {column.name: getattr(vehicle, column.name) for column in models.Vehicle.__table__.columns}

    # Define features
    categorical_features = ["CarName", "fueltype", "aspiration", "carbody", "drivewheel", "enginelocation", "enginetype", "fuelsystem"]
    numerical_features = ["symboling", "doornumber", "wheelbase", "carlength", "carwidth", "carheight", "curbweight", "cylindernumber", "enginesize", "boreratio", "stroke", "compressionratio", "horsepower", "peakrpm", "citympg", "highwaympg"]

    # Encode categorical features
    encoded_feature = []
    for feature in categorical_features:
        encoded = label_encoder.fit_transform([data_dict[feature]])
        encoded_feature.append(encoded[0])

    all_features = encoded_feature + [data_dict[feature] for feature in numerical_features] + [0]
    features = np.array(all_features).reshape(1, -1)

    # Predict price
    predicted_price = predict_model.predict(features)
    vehicle.price = float(predicted_price[0])
    db.commit()

    print(f"Predicted price for vehicle ID {vehicle_id}: {predicted_price[0]}")
    return {"Price_of_car": float(predicted_price[0])}

def callback(ch, method, properties, body):
    vehicle_id = int(body.decode())
    print(f"Received message with vehicle ID: {vehicle_id}")
    db = next(get_db())
    try:
        result = process_vehicle_id(vehicle_id, db)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error processing vehicle ID {vehicle_id}: {e}")
    finally:
        db.close()

def main():
    print("Connecting to RabbitMQ...")
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
    connection_parameters = pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue='vehicle_queue')
    print("Connected to RabbitMQ, waiting for messages...")

    # Set up consumer
    channel.basic_consume(queue='vehicle_queue', on_message_callback=callback, auto_ack=True)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("Consumer stopped")
    finally:
        connection.close()

if __name__ == "__main__":
    print("Starting consumer...")
    main()

