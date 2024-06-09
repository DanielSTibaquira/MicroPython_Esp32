from machine import Pin  # Import Pin class to control GPIO pins
from time import sleep   # Import sleep function to add delays
import dht               # Import dht module for DHT sensors
import network           # Import network module to manage WiFi connections
import utime             # Import utime module to handle time-related functions

sensor = dht.DHT22(Pin(14))  # Initialize DHT22 sensor on GPIO pin 14
led = Pin(2, Pin.OUT)        # Initialize an LED on GPIO pin 2 as output
bandera = 0                  # Initialize a flag variable

ssid = ''  # WiFi SSID
pw = ''    # WiFi password

WIFI = network.WLAN(network.STA_IF)  # Initialize WiFi in station mode
WIFI.active(True)  # Activate the WiFi interface
WIFI.connect(ssid, pw)  # Connect to the specified WiFi network

while not WIFI.isconnected():  # Wait until connected to WiFi
    print("conectando......")
    sleep(1)

estado = WIFI.ifconfig()  # Get network configuration
print(estado)

with open("datos.txt", "w") as arch:  # Open file to log data
    arch.write("Inicio del registro\n")

def paro(pin):  # Function to handle button press
    arch.close()

pulsador = Pin(15, Pin.IN)  # Initialize button on GPIO pin 15 as input
pulsador.irq(trigger=Pin.IRQ_RISING, handler=paro)  # Set interrupt on button press

with open("datos.txt", "w") as arch:  # Open file to log data

    while True:
        try:
            sleep(2)  # Wait 2 seconds before reading
            sensor.measure()  # Trigger measurement
            temp = sensor.temperature()  # Read temperature in Celsius
            hum = sensor.humidity()  # Read humidity percentage

            with open("datos.txt", "a") as arch:  # Append data to file
                temp_str = '%3.1f' % temp
                hum_str = '%3.1f %%' % hum
                localtime = utime.localtime()
                date_str = '%04d-%02d-%02d' % (localtime[0], localtime[1], localtime[2])
                time_str = '%02d:%02d:%02d' % (localtime[3], localtime[4], localtime[5])
                print('Temperatura ;' + temp_str + ';' + 'Humedad ;' + hum_str + ';' + 'Fecha ;' + date_str + ';' + 'Hora ;' + time_str + ';')
                arch.write('Temperatura ;' + temp_str + ';' + 'Humedad ;' + hum_str + ';' + 'Fecha ;' + date_str + ';' + 'Hora ;' + time_str + '\n')
                print(utime.localtime())

            if bandera == 1:
                print("cerre el archivo")
                arch.close()
                bandera = 0

        except OSError as e:  # Handle sensor read failure
            print('Error al leer el sensor:', e)
