from machine import Pin, ADC  # Import Pin and ADC classes to control GPIO pins and analog-to-digital conversion
from time import sleep        # Import sleep function to add delays
import network                # Import network module to manage WiFi connections
import socket                 # Import socket module for networking

ssid = ''  # WiFi SSID
pw = ''    # WiFi password
led = Pin(2, Pin.OUT)  # Initialize an LED on GPIO pin 2 as output
volume = ADC(Pin(34))  # Initialize ADC on GPIO pin 34
volume.atten(ADC.ATTN_11DB)  # Set ADC attenuation for wider input range

valorpot = "0"  # Initialize variable to store potentiometer value

WLAN = network.WLAN(network.STA_IF)  # Initialize WiFi in station mode
WLAN.active(True)  # Activate the WiFi interface
WLAN.connect(ssid, pw)  # Connect to the specified WiFi network

while not WLAN.isconnected():  # Wait until connected to WiFi
    print("conectando......")
    sleep(1)

estado = WLAN.ifconfig()  # Get network configuration
print(estado)

def pagina():  # Define function to generate HTML page
    html = """ <html>
    <head>
    <meta charset='utf-8'/>
    <title>Servidor WEB</title>
    </head>
    <body>
    <h1>HOLA IUE</h1>
    <p><a href='/on'><button>ON</button></a>
    <p><strong id="elvalor">""" + valorpot + """</strong></p>
    </body>
    </html>"""
    return html

elservidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP/IP socket
elservidor.bind(('', 80))  # Bind the socket to port 80
elservidor.listen(5)  # Listen for incoming connections

while True:
    conex, addr = elservidor.accept()  # Accept a connection
    reque = conex.recv(1024)  # Receive the request
    reque = str(reque)
    if reque.find('/on') == 6:  # Check if the request is to turn the LED on
        led.on()
    valor = volume.read()  # Read the ADC value
    valorpot = str(valor)  # Convert the value to a string
    Web = pagina()  # Generate the HTML page
    conex.send('HTTP/1.1 200 OK\n')  # Send HTTP headers
    conex.send('Content-Type: text/html\n')
    conex.send('Connection: close\n\n')
    conex.sendall(Web)  # Send the HTML page
    conex.close()  # Close the connection
