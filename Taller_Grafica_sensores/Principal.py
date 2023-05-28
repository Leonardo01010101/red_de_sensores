# -*- coding: utf-8 -*-
"""
Created on Fri May 26 18:38:54 2023

@author: Leonardo Abello
"""

import os
import sys
from PyQt5 import QtCore, QtGui, Qt, QtWidgets, uic
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
import numpy as np

class Principal(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Principal, self).__init__()
        uic.loadUi('Principal.ui',self)
        
        self.Bt_1.clicked.connect(self.a)
        self.Bt_2.clicked.connect(self.b)
        self.Radio_Bt_1.clicked.connect(self.c)
        self.Radio_Bt_2.clicked.connect(self.d)
        
    def a(self):
        plt.plot([1,2,3,4,5,6,7,8,9],'b*' )
        plt.ylabel('Temperatura')
        plt.xlabel('Sample')
        plt.show()
        
    def b(self):
        x = np.linspace(0, 2 * np.pi, 400)
        y = np.sin(x ** 2)
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
        ax1.plot(x,y)
        ax1.set_ylabel('Radiation (W/m^2)')
        ax2.plot(x,y,'tab:orange')
        ax2.set_ylabel('Temperatura(°C)')
        ax3.plot(x, -y,'tab:green')
        ax3.set_ylabel('Relative Humidity (%)')
        ax3.set_xlabel('Datos')
        plt.show()
        
    def c(self):
        self.Label_1.setText(str(3242))
        self.Label_2.setPixmap(QtGui.QPixmap('./imagenes/casa.png'))
   
    def d(self):
        self.Label_1.setText(str(self.comboBox.currentText()))
           
        
def main():
    print('inicia') 
    app=QtWidgets.QApplication(sys.argv)
    ventana=Principal()
    ventana.show()
    sys.exit(app.exec_())
    
if __name__=='__main__':
    main()    
    