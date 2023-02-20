#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import  QApplication,QMainWindow
from PyQt5.uic import loadUi
from fecha import FechaDeHoy
#from gestion_pedidos import Gestion_pedidos
#from deposito import Deposito
from contactos import Contactos
sys.path.append("db")
from bbdd import Bbdd

class teckel(QMainWindow):
	def __init__(self):
		super(teckel, self).__init__()
		loadUi('./assets/gui/inicio.ui', self)
		#self.btn_gestion.clicked.connect(self.gestionar)
		#self.btn_deposito.clicked.connect(self.abrir_deposito)
		self.btn_contactos.clicked.connect(self.abrir_contactos)
		hoy=FechaDeHoy().fecha_actual()
		self.fecha_hoy.setText(f'Hoy es {hoy[0]} {hoy[1]}\nde {hoy[2]}\n de {hoy[3]}')
		Bbdd().create()
		
		
#Funciones
	
	#Abrir ventana Gestion
	""" def gestionar(self):
		ventana=Gestion_pedidos(self)
		ventana.show()
		
	#Abrir ventana deposito
	def abrir_deposito(self):
		ventana=Deposito(self)
		ventana.show() 
		"""

	#Abrir ventana contactos
	def abrir_contactos(self):
		ventana=Contactos(self)
		ventana.show()  

if __name__=='__main__':
	app = QApplication(sys.argv)
	app.setStyle('Fusion')
	main = teckel()
	main.show()
	sys.exit(app.exec_())