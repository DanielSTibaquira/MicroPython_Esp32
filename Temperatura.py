from machine import Pin  # Import Pin class to control GPIO pins
from time import sleep   # Import sleep function to add delays
import dht               # Import dht module for DHT sensors

sensor = dht.DHT22(Pin(14))  # Initialize DHT22 sensor on GPIO pin 14
# sensor = dht.DHT11(Pin(14))  # Use this line for DHT11 sensor on GPIO pin 14

while True:
  try:
    sleep(2)  # Wait 2 seconds before reading
    sensor.measure()  # Trigger measurement
    temp = sensor.temperature()  # Read temperature in Celsius
    hum = sensor.humidity()  # Read humidity percentage
    temp_f = temp * (9/5) + 32.0  # Convert temperature to Fahrenheit
    print('Temperature: %3.1f C' % temp)
    print('Temperature: %3.1f F' % temp_f)
    print('Humidity: %3.1f %%' % hum)
  except OSError as e:
    print('Failed to read sensor.')  # Handle sensor read failure
