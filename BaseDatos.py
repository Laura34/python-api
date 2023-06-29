from mysql.connector import Error
from mysql.connector import connect
import requests


class Conexion:
    def __init__(self):
        self.database = 'bancos'

    def conectar(self, user, password, host):
        try:
            self.connection = connect(
                host=host,
                user=user,
                password=password,
                database=self.database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                return '¡Conexión Exitosa!'
        except Error as e:
            return ('Error en la conexión con la base de datos' +'\n'+  str(e))


    def leer(self):
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            try:
                self.cursor.execute("""SELECT * FROM datos;""")
            except Error as e:
                return "¡Error!" + '\n' + str(e)
            estudiantes = self.cursor.fetchall()
            return estudiantes

    def insertar(self):
        if self.connection.is_connected():
            url = 'https://random-data-api.com/api/v2/banks'
            response = requests.request("GET", url)
            nombre = response.json()['bank_name']
            ruta = response.json()['routing_number']
            iban = response.json()['iban']
            self.cursor = self.connection.cursor()
            parametros = "'" + nombre + "', '" + ruta + "', '" + iban + "'"
            print(parametros)
            consulta = "INSERT INTO datos (nombre, ruta, iban) VALUES ("+ parametros + ");"
            try:
                self.cursor.execute(consulta)
            except Error as e:
                return "¡Error!" + '\n' + str(e)
            self.connection.commit()
            return '¡Éxito!'
