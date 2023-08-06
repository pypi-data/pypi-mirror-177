from flask import Flask, request, jsonify, make_response
from flask_compress import Compress
from influxdb import InfluxDBClient, client
from urllib import parse
import json

class HomeServices:

    def __init__(self,  template_folder, static_folder):
        self.app = Flask(__name__,  template_folder=template_folder, static_folder=static_folder)
        self.app.add_url_rule('/', 'index', self.index, methods=['GET'])
        self.app.add_url_rule('/alexaintent', 'alexaintent', self.alexa_intent, methods=['GET'])
        self.app.add_url_rule('/customsensor', 'customsensor', self.custom_sensor, methods=['GET'])
        Compress(self.app)

        host = 'pi02'
        user = 'writer'
        password = '24$Qw7LVRjOI'
        bucket = 'hometelemetry'

        self.influx_conn = InfluxDBClient(host=host, username=user, password=password, database=bucket)

    def getApp(self):
        return self.app

    def run(self):
        self.app.run()
        #self.app.run(host='0.0.0.0')

    def index(self):
        return 'This is the Pi server.'

    def custom_sensor(self):
        if request.method == 'GET':
            # Parse GET param
            sensor = parse.parse_qs(parse.urlparse(request.url).query)['sensor'][0]

            sensor_table = {'jardín': 2, 'cocina': 1, 'buhardilla': 3}

            if sensor in sensor_table.keys():
                query = "SELECT * from DHT22 WHERE sensorid='{}' ORDER BY time DESC LIMIT 1".format(sensor_table[sensor])
                result_set = self.influx_conn.query(query)
                point = list(result_set.get_points())[0]

            response = make_response(json.dumps('{{"temp" : {}, "hum" : {} }}'.format(point['temp'], point['humidity'])))
            response.mimetype = "application/json"
            response.headers['Pragma'] = 'no-cache'
            response.headers["Expires"] = 0
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            return response


    def alexa_intent(self):
        if request.method == 'GET':
            # Parse GET param
            sensor = parse.parse_qs(parse.urlparse(request.url).query)['sensor'][0]

            sensor_table = {'jardín': 2, 'cocina': 1, 'buhardilla': 3}

            if sensor in sensor_table.keys():
                query = "SELECT * from DHT22 WHERE sensorid='{}' ORDER BY time DESC LIMIT 4".format(sensor_table[sensor])
                result_set = self.influx_conn.query(query)
                points = list(result_set.get_points())

                trend = ''
                if len(points) == 4:
                    delta = points[0]['temp'] - points[3]['temp']
                    if delta > 0.1:
                        trend = ' y subiendo ligeramente'
                    elif delta > 0.3:
                        trend = ' y subiendo'
                    elif delta > 0.6:
                        trend = ' y subiendo a saco'
                    elif delta < -0.1:
                        trend = ' y bajando ligeramente'
                    elif delta < -0.3:
                        trend = ' y bajando'
                    elif delta < -0.6:
                        trend = ' y bajando a saco'

                response_dict = "Hace {} grados{}, y la humedad es del {:.0f} por ciento."\
                                .format(points[0]['temp'], trend, points[0]['humidity'])

                if points[0]['humidity'] > 98:
                    response_dict += " Es muy posible que esté lloviendo."

                if points[0]['temp'] < 5:
                    response_dict += " ¡Joder, que frio hace!."
                elif points[0]['temp'] < 10:
                    response_dict += " Hace bastante fresquete."
                elif points[0]['temp'] > 30:
                    response_dict += " ¡Que calor hace!."
                elif points[0]['temp'] > 35:
                    response_dict += " ¡Joder, que nos achicharramos!."
            else:
                response_dict = "Ese sensor es desconocido"

            response = make_response(response_dict.encode('UTF-8'))
            response.mimetype = "text/plain"
            response.headers['Pragma'] = 'no-cache'
            response.headers["Expires"] = 0
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            return response


