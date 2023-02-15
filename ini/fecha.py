from datetime import datetime, date

class FechaDeHoy():
    def __init__(self):
        self.dia_semana=date.today().weekday()
        self.hoy= datetime.now()
        
    def fecha_actual(self):
        nombre_dia=['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        dia=self.hoy.day
        mes=self.hoy.month
        nombre_mes=['Enero',
                'Febrero',
                'Marzo',
                'Abril',
                'Mayo',
                'Junio',
                'Julio',
                'Agosto',
                'Septiembre',
                'Octubre',
                'Noviembre',
                'Diciembre']
        año= self.hoy.year
        fecha_de_hoy=[nombre_dia[self.dia_semana],dia, nombre_mes[mes-1],año]
        return fecha_de_hoy
