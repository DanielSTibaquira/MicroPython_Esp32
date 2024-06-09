from machine import Pin  # Import Pin class to control GPIO pins
from time import sleep   # Import sleep function to add delays
import dht               # Import dht module for DHT sensors
from umqtt import MQTTClient  # Import MQTTClient for MQTT communication
import network           # Import network module to manage WiFi connections
import socket            # Import socket module

# MQTT configuration for IoT Panel
tokenAPI = ""
clienteID = ""
servidor = "broker.emqx.io"  # MQTT broker address
puerto = 1883  # MQTT broker port
usuario = ""
contrasena = ""
led = Pin(2, Pin.OUT)  # Initialize an LED on GPIO pin 2 as output

ssid = ''  # WiFi SSID
pw = ''    # WiFi password

WLAN = network.WLAN(network.STA_IF)  # Initialize WiFi in station mode
WLAN.active(True)  # Activate the WiFi interface
WLAN.connect(ssid, pw)  # Connect to the specified WiFi network

while not WLAN.isconnected():  # Wait until connected to WiFi
    print("conectando......")
    sleep(1)

estado = WLAN.ifconfig()  # Get network configuration
print(estado)

cliente = MQTTClient(clienteID, servidor)  # Initialize MQTT client
cliente.connect()  # Connect to the MQTT broker

print("OK conectado")

Sensor = dht.DHT22(Pin(14))  # Initialize DHT22 sensor on GPIO pin 14

while True:
    try:
        sleep(2)  # Wait 2 seconds before reading
        Sensor.measure()  # Trigger measurement
        T = Sensor.temperature()  # Read temperature in Celsius
        H = Sensor.humidity()  # Read humidity percentage
        print("Temp", T)
        print("Hum", H)
        
        # Publish temperature data to MQTT broker
        msg = b'{"Temperatura":{"value":%s}}' % (T)
        cliente.publish(b"Temperatura", msg)
        print(msg)
        
        # Publish humidity data to MQTT broker
        msgH = b'{"Humedad":{"value":%s}}' % (H)
        cliente.publish(b"Humedad", msgH)
        print(msgH)
    except OSError as e:  # Handle sensor read failure
        print("NO puedo leer")
