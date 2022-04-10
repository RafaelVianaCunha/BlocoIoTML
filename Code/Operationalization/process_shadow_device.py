from curses import qiflush
import re
from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
from datetime import date, datetime, timedelta
import numpy as np
import random 
import pandas as pd

import time as t
import json

SENSOR_FILE = "../../Data/Modeling/airpollutiondelhidataset.csv"
ENDPOINT = "a26zsebtxwswfs-ats.iot.us-east-2.amazonaws.com"
CLIEND_ID = "sensor"
PATH_TO_CERTIFICATE = "../Certificates/sensor.cert.pem"
PATH_TO_PRIVATE_KEY = "../Certificates/sensor.private.key"
PATH_TO_AMAZON_ROOT_CA_1 = "../Certificates/root-CA.crt"

TOPIC = "$aws/things/sensor/shadow/name/air_quality_shadow/update"

df = pd.read_csv(SENSOR_FILE)
df.date = pd.to_datetime(df.date)
df = df.set_index('date')

def classify_pm25(val):
    if(val <= 30):
        return 1
    elif(val > 30 and val <= 60):
        return 2
    elif (val > 60 and val <= 90):
        return 3
    elif (val > 90 and val <= 120):
        return 4
    elif (val > 120 and val <= 250):
        return 5
    elif (val > 250):
        return 6

def classify_pm10(val):
    if(val <= 50):
        return 1
    elif (val > 50 and val <= 100):
        return(2)
    elif (val > 100 and val <= 250):
        return 3
    elif (val>250 and val <= 350):
        return 4
    elif (val > 350 and val <= 430):
        return 5
    elif (val > 430):
        return 6

def find_metric_avarage(df, col):
    data = df[[col]].sort_values(by='date').copy()

    if((data.index.max() - timedelta(7))):
        last_15_days = data[-14:]      
        avg = last_15_days[col].mean()

        return np.round(avg, 2)

def get_air_quality_state(aqi):
    state = {
        1: 'Bom',
        2: 'Satisfatório',
        3: 'Moderado',
        4: 'Baixa',
        5: 'Muito baixa',
        6: 'Critico'
    }

    return state[aqi]
    
def get_payload(df):
    payload_model = {
        "state": {
            "desired": {
                "aqi_pm10": "",
                "aqi_pm25": "",
                "aqi_pm10_index": "",
                "aqi_pm25_index": "",
                "description_pm10": "",
                "description_pm25": ""
            }
        }
    }

    pm10_average_last_days = find_metric_avarage(df, "pm10")
    pm25_average_last_days = find_metric_avarage(df, "pm25")
    avarage_pm10_classified = classify_pm10(pm10_average_last_days)
    avarage_pm25_classified = classify_pm25(pm25_average_last_days)

    pm10_index = random.randint(0, 500)
    current_pm10 = classify_pm10(pm10_index)
    payload_model['state']['desired']['aqi_pm10_index'] = pm10_index
    payload_model['state']['desired']['aqi_pm10'] = get_air_quality_state(current_pm10)

    pm25_index = random.randint(0, 300)
    current_pm25 = classify_pm25(pm25_index)
    payload_model['state']['desired']['aqi_pm25_index'] = pm25_index
    payload_model['state']['desired']['aqi_pm25'] = get_air_quality_state(current_pm25)

    if (current_pm10 > avarage_pm10_classified):
        payload_model['state']['desired']['description_pm10'] = 'Qualidade do ar está pior. Por favor, usem máscara'
    elif (current_pm10 < avarage_pm10_classified):
        payload_model['state']['desired']['description_pm10'] = 'Qualidade do ar está melhor, porém contiuem se cuidando'
    else:
        payload_model['state']['desired']['description_pm10'] = 'Qualidade do ar não mudou desde os últimos 15 dias'

    if (current_pm25 > avarage_pm25_classified):
        payload_model['state']['desired']['description_pm25'] = 'Qualidade do ar está pior. Por favor, usem máscara'
    elif (current_pm25 < avarage_pm25_classified):
        payload_model['state']['desired']['description_pm25'] = 'Qualidade do ar está melhor, porém contiuem se cuidando'
    else:
        payload_model['state']['desired']['description_pm25'] = 'Qualidade do ar não mudou desde os últimos 15 dias'

    return payload_model

if __name__ == "__main__":
    stop = True
    payload = get_payload(df)
    event_loop_group = io.EventLoopGroup(1)
    host_resolver = io.DefaultHostResolver(event_loop_group)
    client_bootstrap = io.ClientBootstrap(event_loop_group,  host_resolver)
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=ENDPOINT,
        cert_filepath=PATH_TO_CERTIFICATE,
        pri_key_filepath=PATH_TO_PRIVATE_KEY,
        ca_filepath=PATH_TO_AMAZON_ROOT_CA_1,
        client_bootstrap=client_bootstrap,
        client_id=CLIEND_ID,
        clean_session=False,
        keep_alive_secs=6
    )
    connection_future = mqtt_connection.connect()
    connection_future.result()
    while stop:
        payload = get_payload(df)
        print("Sending message to topic: {}".format(payload))
        
        mqtt_connection.publish(
            topic=TOPIC,
            payload=json.dumps(payload),
            qos=mqtt.QoS.AT_LEAST_ONCE)
        
        t.sleep(.1)

    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()