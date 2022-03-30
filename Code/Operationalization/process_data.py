from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder
import csv

import re
import time as t
import json

SENSOR_FILE = "../../Data/Processed/air_pol_delhi.csv"
ENDPOINT = "a26zsebtxwswfs-ats.iot.us-east-2.amazonaws.com"
CLIEND_ID = "sensor"
PATH_TO_CERTIFICATE = "../Certificates/sensor.cert.pem"
PATH_TO_PRIVATE_KEY = "../Certificates/sensor.private.key"
PATH_TO_AMAZON_ROOT_CA_1 = "../Certificates/root-CA.crt"

TOPIC = "sensor/data"

def create_payload(row):
    return {
        "city": row[0],
        "name": row[1],
        "date": row[2],
        "pm25": row[3],
        "pm10": row[4],
        "so2": row[5],
        "co": row[6],
        "ozone": row[7],
    }

if __name__ == "__main__":
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

    with open(SENSOR_FILE) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            payload = create_payload(row)
            print("Sending message to Aws Iot Core: {}".format(payload))
            
            mqtt_connection.publish(
                topic=TOPIC,
                payload=json.dumps(payload),
                qos=mqtt.QoS.AT_LEAST_ONCE)
            
            t.sleep(.1)
    
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
