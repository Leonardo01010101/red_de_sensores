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

def main():
    import sys
    print("inicia")
    app=QtWidgets.QApplication(sys.argv)
    ventana=Graficas_Taller_sensor()
    ventana.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main()
    
