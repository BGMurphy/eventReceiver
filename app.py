import connexion
from connexion import NoContent
import requests
import pykafka
from pykafka import KafkaClient
import datetime
import json
import yaml
from flask_cors import CORS, cross_origin
import logging
import logging.config

with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

#STORE_SURGERY_INFO_REQUEST_URL = "http://localhost:8090/report/book_surgery"
#STORE_XRAY_REPORT_REQUEST_URL = "http://localhost:8090/report/xRay"
HEADERS = {"content-type":"application/json"}

def book_surgery(surgeryInfo):
    #response = requests.post(STORE_SURGERY_INFO_REQUEST_URL, json=surgeryInfo, headers=HEADERS)
    print(surgeryInfo)
    kafka = app_config['datastore']['server'] + ':' + app_config['datastore']['port']
    client = KafkaClient(hosts=kafka)
    topic = client.topics[app_config['datastore']['topic']]
    producer = topic.get_sync_producer()
    msg = { "type": "surgeryInfo",
            "datetime" : datetime.datetime.now().strftime("%Y -%m-%dT%H:%M:%S"),
            "payload" : surgeryInfo }
    msg_str = json.dumps(msg)
    logger.info(msg_str.encode('utf-8'))
    producer.produce(msg_str.encode('utf-8'))

    return NoContent, 201

def xRay_report(report):
    #response = requests.post(STORE_XRAY_REPORT_REQUEST_URL, json=report, headers=HEADERS)
    print(report)
    kafka = app_config['datastore']['server'] + ':' + app_config['datastore']['port']
    client = KafkaClient(hosts=kafka)
    topic = client.topics[app_config['datastore']['topic']]
    producer = topic.get_sync_producer()
    msg = { "type": "xrayInfo",
            "datetime" : datetime.datetime.now().strftime("%Y -%m-%dT%H:%M:%S"),
            "payload" : report }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    logger.info(msg_str.encode('utf-8'))

    return NoContent, 201

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api("openapi.yaml")
CORS(app.app)
app.app.config['CORS_HEADERS'] = 'Content-Type'

try:
    with open('/config/app_conf.yaml', 'r') as f:
        app_config = yaml.safe_load(f.read())
except:
    with open('app_conf.yaml', 'r') as f:
        app_config = yaml.safe_load(f.read())

if __name__ == "__main__":
    app.run(port=8080)