#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QMainWindow, QLabel, QTableWidgetItem, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtCore import QRegularExpression
from PyQt5.QtGui import QRegularExpressionValidator,QIntValidator
from fecha import FechaDeHoy
# Hay que ejecutar esta línea antes de importar el módulo.
sys.path.append("db")
from bbdd import Bbdd

class Contactos(QMainWindow):
    def __init__(self, parent=None):
        super(Contactos, self).__init__(parent)
        loadUi('./assets/gui/contactos.ui', self)

        #fecha actual en statusBar
        fecha=FechaDeHoy().fecha_actual()
        hoy=f'Hoy es {fecha[0]} {fecha[1]} de {fecha[2]} de {fecha[3]}'
        self.fecha_statusbar = QLabel(f"{hoy}")
        self.statusBar.addPermanentWidget(self.fecha_statusbar)

    #Listas
        #Contactos
        tipo_contacto=['','Cliente', 'Proveedor']
        self.tipo_contacto.addItems(tipo_contacto)
                
        #Tipos de documentos
        doc=['','CUIT','DNI']
        self.tipo_doc.addItems(doc)
    
    # Establecer ancho de las columnas
        #Tabla de contactos
        for indice, ancho in enumerate((155, 285, 150), start=0):
            self.tabla_contactos.setColumnWidth(indice, ancho)

    #Variable global de cuit vigente para realizar cambios en los datos de ese cuit incluso cambios en el mismo
        self.cuit_vigente = []
        
    #Configuracion 			
        #Señales
        self.buscador.returnPressed.connect(self.buscar_existente)
        self.tabla_contactos.itemClicked.connect(self.recuperar_datos)
        self.tipo_contacto.currentIndexChanged.connect(self.insertar_nombre)
        self.tipo_doc.currentIndexChanged.connect(self.conf_numero)
        self.nombre.textChanged[str].connect(self.formato_nombre)
        self.direccion.textChanged[str].connect(self.formato_direccion)
        self.email.textChanged[str].connect(self.formato_mail)

        #Señales de botones Botones
        self.btn_nuevo.clicked.connect(self.nuevo)
        self.btn_guardar.clicked.connect(self.guardar_contacto)
        self.btn_editar.clicked.connect(self.editar_contacto)
        self.btn_limpiar.clicked.connect(self.limpiar_pantalla)

    #Funciones
    #Crear nuevo contacto
    def nuevo (self):
        self.limpiar_pantalla()
        self.btn_nuevo.setEnabled(False)
        self.btn_guardar.setEnabled(True)
        self.grupo_contacto.setEnabled(True)
        self.tipo_contacto.setEnabled(True)
        self.tipo_doc.setEnabled(True)
        self.direccion.setEnabled(True)
        self.telefono.setEnabled(True)
        self.telefono2.setEnabled(True)
        self.telefono3.setEnabled(True)
        self.email.setEnabled(True)

    #Habilitar carga de nombre
    def insertar_nombre(self):
        tipo_contacto = self.tipo_contacto.currentText()
        #Si está vacio no se habilita el ingreso de datos en la casilla "nombre" 
        if tipo_contacto == '':
            self.nombre.setEnabled(False)
            self.nombre.setText('')
        else:
            self.nombre.setText('')
            self.nombre.setEnabled(True)

    #Número segun tipo de documento
    def conf_numero(self):
        tipo_doc=self.tipo_doc.currentText()
        if tipo_doc=='DNI':
            self.numero.setEnabled(True)
            self.numero.setText('')
            self.numero.setMaxLength(8)
            conf = QRegularExpressionValidator(self)
            conf.setRegularExpression(QRegularExpression("(^[1-9][0-9]*(:[1-9][0-9]*)?$)?"))
            self.numero.setValidator(conf)
        elif tipo_doc=='':
            self.numero.setEnabled(False)
            self.numero.setText('')
        else:
            self.numero.setEnabled(True)
            self.numero.setText('')
            self.numero.setMaxLength(11)
            conf = QRegularExpressionValidator(self)
            conf.setRegularExpression(QRegularExpression("(^[1-9][0-9]*(:[1-9][0-9]*)?$)?"))
            self.numero.setValidator(conf)

    #Guardar datos del nuevo contacto
    def guardar_contacto(self):
        tipo=self.tipo_contacto.currentText()
        nombre= self.nombre.text()
        tipo_doc=self.tipo_doc.currentText()
        numero=self.numero.text()
        direccion=self.direccion.text()
        telefono=self.telefono.text()
        telefono2=self.telefono2.text()
        telefono3=self.telefono3.text()
        email=self.email.text()
        if self.cuit_vigente == None or self.cuit_vigente==[]:
            datos=[numero, nombre, direccion, telefono, telefono2, telefono3, email]
            if  nombre == '' or  numero == '' or direccion =='' or telefono =='':
                QMessageBox.warning(self, 'Error', '<font size = 5><b>Faltan datos</b></font size>')
            else:
                query=f'INSERT INTO {tipo} VALUES(?,?,?,?,?,?,?)'
                Bbdd().insert_delete_update(query, datos)
                QMessageBox.information(self, "Nuevo contacto", "<font size = 5><b>Se agregó correctamente el contacto</b></font size>" , QMessageBox.Ok, QMessageBox.Ok)
                self.limpiar_pantalla()
        else:
            if (tipo_doc == 'DNI' and len(str(numero))== 8) or (tipo_doc == 'CUIT' and len(str(numero))== 11):
                query=f'UPDATE {tipo} SET cuit=?, descripcion=?, domicilio=?, telefono_1=?, telefono_2=?, telefono_3=?, mail=? WHERE cuit=?'
                datos=[numero, nombre, direccion, telefono, telefono2, telefono3, email, self.cuit_vigente[0]]
                Bbdd().insert_delete_update(query,datos)
                QMessageBox.information(self, "Modificacíon", "<font size = 5><b>Se modificó correctamente el contacto</b></font size>" , QMessageBox.Ok, QMessageBox.Ok)
                self.limpiar_pantalla()
            else:
                QMessageBox.warning(self, 'ERROR DNI/CUIT', '<font size = 5><b>Verificar cantidad de dígitos en el número de DNI/CUIT. <br><pre>- Para DNI, deben ser 8 dígitos.</pre><pre>- Para CUIT, deben ser 11 dígitos.</pre></b></font size>')


    #Editar contacto existente    
    def editar_contacto (self):
        if self.numero.text()=='':
            QMessageBox.warning(self, 'Error', '<font size = 5><b>No se registran datos para editar.\nSeleccione un contacto y vuelva a intentarlo</b></font size>')
        else:
            self.btn_nuevo.setEnabled(False)
            self.btn_eliminar.setEnabled(False)
            tipo=self.tipo_contacto.currentText()
            if tipo!='' or tipo!=None: 
                self.cuit_vigente = [self.numero.text()]
                self.btn_guardar.setEnabled(True)
                self.grupo_contacto.setEnabled(True)
                self.tipo_contacto.setEnabled(False)
                self.tipo_doc.setEnabled(False)
                self.numero.setEnabled(True)
                self.direccion.setEnabled(True)
                self.telefono.setEnabled(True)
                self.telefono2.setEnabled(True)
                self.telefono3.setEnabled(True)
                self.email.setEnabled(True)
                return self.cuit_vigente
            else:
                QMessageBox.warning(self, 'Error', '<font size = 5><b>Debe ingresar el tipo de contacto</b></font size>')

    #Busqueda inicial
    def buscar_existente (self):
        self.grupo_contacto.setEnabled(False)
        self.btn_guardar.setEnabled(False)
        buscador=[f'%{self.buscador.text()}%']
        tipo_contacto = ['proveedor', 'cliente']
        n=0
        for contacto in tipo_contacto:
            query=f'SELECT cuit, descripcion FROM {contacto} WHERE  descripcion LIKE ? '
            fetch='fetchall'
            resultado=Bbdd().select(query,buscador, fetch)
            for i in resultado:
                self.tabla_contactos.setRowCount(n + 1)
                self.tabla_contactos.setItem(n, 0, QTableWidgetItem(str(i[0])))
                self.tabla_contactos.setItem(n, 1, QTableWidgetItem(i[1]))
                self.tabla_contactos.setItem(n, 2, QTableWidgetItem(contacto.title()))
                n+=1

    #Datos de Busqueda
    def recuperar_datos(self):
        self.grupo_contacto.setEnabled(False)
        self.btn_guardar.setEnabled(False)
        #selecion de la tabla
        seleccion=self.tabla_contactos.selectedItems()
        #Lo segun tipo de cliente es si dividimos el nombre o no
        self.btn_eliminar.setEnabled(True)
        self.btn_editar.setEnabled(True)		
        id_contacto=[int(f'{seleccion[0].text()}')]
        query=f'SELECT * FROM {seleccion[2].text()} WHERE cuit=?'
        fetch='fetchone'
        resultado=Bbdd().select(query,id_contacto, fetch)
        self.tipo_contacto.setCurrentText(seleccion[2].text().title())
        self.nombre.setText(resultado[1])
        if len(str(resultado[0])) == 8:
            self.tipo_doc.setCurrentText('DNI')
        else:
            self.tipo_doc.setCurrentText('CUIT')
        self.numero.setText(str(resultado[0]))
        self.direccion.setText(resultado[2])
        self.telefono.setText(resultado[3])
        self.telefono2.setText(resultado[4])
        self.telefono3.setText(resultado[5])
        self.email.setText(resultado[6])

    #Eliminar filas de tabla contactos
    def limpiar_filas(self):
        filas=self.tabla_contactos.rowCount()
        for i in range(filas):
            self.tabla_contactos.removeRow(0)
        self.tabla_contactos.clearContents()

    #Vaciar los datos de pantalla            
    def limpiar_pantalla (self):
        self.btn_nuevo.setEnabled(True)
        self.grupo_contacto.setEnabled(False)
        self.btn_guardar.setEnabled(False)
        self.btn_eliminar.setEnabled(False)
        self.btn_editar.setEnabled(False)
        self.buscador.setText('')	
        self.tipo_contacto.setCurrentText('')
        self.nombre.setText('')
        self.tipo_doc.setCurrentText('')
        self.numero.setText('')
        self.direccion.setText('')
        self.telefono.setText('')
        self.telefono2.setText('')
        self.telefono3.setText('')
        self.email.setText('')
        self.limpiar_filas()
        self.cuit_vigente=[]

    #Formato fijado de 1ra letra en mayuscula despues del espacio 
    def formato_nombre(self,text):
        mp=text.title()
        self.nombre.setText(mp)  

    #Formato fijado de 1ra letra en mayuscula despues del espacio 
    def formato_direccion(self,text):
        mp=text.title()
        self.direccion.setText(mp)  

    #Formato fijado para que sea todo minuscula
    def formato_mail(self,text):
        mp=text.lower()
        self.email.setText(mp)  