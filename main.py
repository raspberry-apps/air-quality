import time

from influxdb import InfluxDBClient
from sds011 import SDS011

DB_NAME = 'air_quality'

if __name__ == '__main__':

  def get_reading():
    sensor = SDS011('/dev/ttyUSB0', use_query_mode=True)
    time.sleep(30)
    reading = sensor.query()
    sensor.sleep()
    return reading

  def update_influx(reading):
    json_body = [
      {
          "measurement": DB_NAME,
          "fields": {
              "pm_25": reading[0],
              "pm_10": reading[1]
          }
      }
    ]

    client = InfluxDBClient('localhost', 8086)
    
    try:
      client.create_database(DB_NAME)
    except:
      pass

    client.switch_database(DB_NAME)

    client.write_points(json_body)

    result = client.query('select pm_25, pm_10 from air_quality;')
    print("Result: {0}".format(result))

  reading = get_reading()
  update_influx(reading)