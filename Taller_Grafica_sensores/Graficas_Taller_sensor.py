# -*- coding: utf-8 -*-
"""
Created on Sat May 27 010:13:30 2023

@author: Wilson Leonardo Abello
"""

import os
import sys
import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import math
import images_rc
import RPi.GPIO as GPIO

from PyQt5 import QtCore, QtGui, Qt, QtWidgets, uic
from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode

#from __future__ import print_function
# Python imports
import http.client
import time
import urllib

matplotlib.use("Qt5Agg")

now = datetime.datetime.now()

a= np.arange(1.0, 30.0, 0.5)

s1 = [(ai**2)/100 for ai in a]
s2 = [math.sin(1/2*math.pi*ai) for ai in a]
s3= [math.cosh(3/2*math.pi*ai) for ai in a]
s4 = [abs(math.sin(2*math.pi*ai)) for ai in a]

with open("./datos_sensores.txt", "w") as file:
    for i in range(len(a)):
        file.write(str(now) + " " + str(round(a[i],2)) + " " + str(round(s1[i],5)) + " " + str(s2[i]) + " " + str(s3[i]) + " " + str(s4[i]) + "\n")


class Graficas_Taller_sensor(QtWidgets.QMainWindow):
    def __init__(self):
        super (Graficas_Taller_sensor, self).__init__()
        uic.loadUi("Graficas_Taller.ui",self)
        
        self.Graf1.clicked.connect(self.a)
        self.Graf2.clicked.connect(self.b)
        self.Graf3.clicked.connect(self.c)
        self.Graf4.clicked.connect(self.d)
        self.Graf.clicked.connect(self.e)
        self.Led.clicked.connect(self.f)
        self.Captura_Datos.clicked.connect(self.g)
        self.load_data()
    
    def load_data(self):
    
       data = []
       with open("./datos_sensores.txt", "r") as file:
           for line in file:
               line_data = line.strip().split()
               data.append(line_data)


       self.tableWidget.setColumnCount(len(data[0]))
       self.tableWidget.setRowCount(len(data))
       self.tableWidget.setHorizontalHeaderLabels(["Fecha", "Hora" ,"Tiempo (s)", "sensor1 ", "sensor2", "sensor3", "sensor4"])


       for i, row in enumerate(data):
           for j, item in enumerate(row):
               self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(item))
    
    def a(self):
            plt.plot(s1, "-.b", marker= "*")
            plt.ylabel("sensor 1")
            plt.xlabel("Tiempo(s)")
            plt.show()
    
    def b(self):
            plt.plot(s2, "--g",marker= "o")
            plt.ylabel("sensor 2")
            plt.xlabel("Tiempo(s)")
            plt.show()
   
    def c(self):
            plt.plot(s3, "-b",marker= "*")
            plt.ylabel("sensor 3")
            plt.xlabel("Tiempo(s)")
            plt.show()
   
    def d(self):
            plt.plot(s4, "--r",marker= "o")
            plt.ylabel("sensor 4")
            plt.xlabel("Tiempo(s)")
            plt.show()
            
    def e(self): 
            fig, (ax1, ax2, ax3 ,ax4) = plt.subplots(4, 1)
            ax1.plot(s1)
            ax1.set_ylabel('sensor 1')
            ax2.plot(s2,'tab:green')
            ax2.set_ylabel('sensor 2')
            ax3.plot(s3,'tab:orange')
            ax3.set_ylabel('sensor 3')
            ax4.plot(s4,'tab:black')
            ax4.set_ylabel('sensor 4')
            ax4.set_xlabel('Tiempo (s)')
    def f(self):
            # Pin assignments
            LED_PIN = 7
            BUTTON_PIN = 17
            # Setup GPIO module and pins
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(LED_PIN, GPIO.OUT)
            GPIO.setup(BUTTON_PIN, GPIO.IN)
            # Set LED pin to OFF (no voltage)
            GPIO.output(LED_PIN, GPIO.LOW)
            try:
                # Loop forever
                while 1:
                    # Detect voltage on button pin
                    if GPIO.input(BUTTON_PIN) == 1:
                        # Turn on the LED
                        GPIO.output(LED_PIN, GPIO.HIGH)
                    else:
                        # Turn off the LED
                        GPIO.output(LED_PIN, GPIO.LOW)
            
            except KeyboardInterrupt:
                print('Hecho')
            finally:
                GPIO.cleanup()            
    def g(self): 
            print()  
 #############################ADQUISICION DE DATOS DEL SENSOR##############################
            # Serial port on Raspberry Pi
            SERIAL_PORT = "/dev/ttyUSB0"  # "/dev/ttyS0"
            # BAUD rate for the XBee module connected to the Raspberry Pi
            BAUD_RATE = 9600
            # The name of the remote node (NI)
            REMOTE_NODE_ID = "SENSOR1"
            # Analog pin we want to monitor/request data
            ANALOG_LINE = IOLine.DIO3_AD3
            # Sampling rate
            SAMPLING_RATE = 15
            # Get an instance of the XBee device class
            device = XBeeDevice(SERIAL_PORT, BAUD_RATE)
            
            # Method to connect to the network and get the remote node by id
            def get_remote_device():
               """Get the remote node from the network 
               Returns:
               """
               # Request the network class and search the network for the remote node
               xbee_network = device.get_network()
               remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
               if remote_device is None:
                  print("ERROR: Remote node id {0} not found.".format(REMOTE_NODE_ID))
                  exit(1)
               remote_device.set_dest_address(device.get_64bit_addr())
               remote_device.set_io_configuration(ANALOG_LINE, IOMode.ADC)
               remote_device.set_io_sampling_rate(SAMPLING_RATE)
            
            def io_sample_callback(sample, remote, time):
               print("Reading from {0} at {1}:".format(REMOTE_NODE_ID, remote.get_64bit_addr()))
               # Calculate supply voltage
               volts = (sample.power_supply_value * (1200.0 / 1024.0)) / 1000.0
               print("\tSupply voltage = {0}v".format(volts))
 #######################ENVIAR DATO AL SERVIDOR#############################
            # API KEY
               THINGSPEAK_APIKEY = 'YQAF62KX12PDTQKB'
               print("Welcome to the ThingSpeak Raspberry Pi Voltage sensor! Press CTRL+C to stop.")
               try:
                  while 1:
                     # Setup the data to send in a JSON (dictionary)
                     params = urllib.parse.urlencode(
                          {
                             'field1': volts,
                             'key': THINGSPEAK_APIKEY,
                          }
                     )
                     # Create the header
                     headers = { "Content-type": "application/x-www-form-urlencoded", 'Accept': "text/plain"}
                     # Create a connection over HTTP
                     conn = http.client.HTTPConnection("api.thingspeak.com:80")
                     try:
                         # Execute the post (or update) request to upload the data
                         conn.request("POST", "/update", params, headers)
                         # Check response from server (200 is success)
                         response = conn.getresponse()
                         # Display response (should be 200)
                         print("Response: {0} {1}".format(response.status,response.reason))
                         # Read the data for diagnostics
                         data = response.read()
                         conn.close()
                     except Exception as err:
                         print("WARNING: ThingSpeak connection failed: {0}, " "data: {1}".format(err, data))
                     # Sleep for 20 seconds
                     time.sleep(20)
               except KeyboardInterrupt:
                     print("Thanks, bye!")
               exit(0)
#########################MOSTRAR DATOS ADQUIRIDOS POR EL SENSOR ##########################
            
            try:
               print("Welcome to example of reading a remote  sensor!")
               device.open() # Open the device class
               # Setup the remote device
               get_remote_device()
               # Register a listener to handle the samples received by the local device.
               device.add_io_sample_received_callback(io_sample_callback)
               while True:
                   pass
            except KeyboardInterrupt:
               if device is not None and device.is_open():
                  device.close()      
           
def main():
    import sys
    print("inicia")
    app=QtWidgets.QApplication(sys.argv)
    ventana=Graficas_Taller_sensor()
    ventana.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()
    
