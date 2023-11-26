import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QFontDatabase, QFont, QPixmap
from PyQt5.QtWidgets import QPushButton, QComboBox, QLineEdit, QMainWindow, QDesktopWidget, QLabel, QApplication, QMessageBox
import re

class registrar1(QMainWindow):
    # Hacer el metodo de construccion de la ventana
    def __init__(self):
        super(registrar1, self).__init__()
        self.setStyleSheet("background-color: #BBFDF8;")
        self.setWindowTitle("Registro")

        # Poner el color  de fondo a la ventana
        self.setWindowIcon(QtGui.QIcon("imagenes/icono1.png"))

        # Estableciendo las propiedades de ancho y alto
        self.ancho = 600
        self.alto = 800

        # Establecer el tamaño de la ventana:
        self.resize(self.ancho, self.alto)

        # Estas lineas hacen que la ventana se vea en el centro:
        self.pantalla = self.frameGeometry()
        self.centro = QDesktopWidget().availableGeometry().center()
        self.pantalla.moveCenter(self.centro)
        self.move(self.pantalla.topLeft())

        # Para que la ventana no se pueda cambiar de tamaño
        # Se fija el ancho y el alto
        self.setFixedWidth(self.ancho)
        self.setFixedHeight(self.alto)
        self.set_background_image("imagenes/fnd1.png")

        # Hacemos el tipo de letra
        self.letra1 = QFont()
        # Le asignamos el tipo de letra descargado
        self.letra1.setFamily("Arial")
        # Le asignamos el tamaño
        self.letra1.setPointSize(18)

        self.letra3 = QFont()
        self.letra3.setFamily("Arial")
        self.letra3.setPointSize(12)
        # Hacemos el tipo de letra
        self.letra2 = QFont()
        # Le asignamos el tipo de letra descargado
        self.letra2.setFamily("Arial")
        # Le asignamos el tamaño
        self.letra2.setPointSize(12)

        # Hacemos el letrero
        self.letrero1 = QLabel(self)
        # Le escribimos el texto
        self.letrero1.setText("Registro")
        # Le asignamos el tipo de letra
        self.letrero1.setFont(self.letra1)
        # Le ponemos color de fondo, color de texto y margenes al letrero
        self.letrero1.setStyleSheet("color: #000000; padding: 40px;")
        self.letrero1.setFixedWidth(400)
        self.letrero1.setFixedHeight(40)

        self.letrero1.move(20, 40)

        # Hacemos el letrero
        self.login = QLabel(self)
        # Le escribimos el texto
        self.login.setText("Usuario")
        # Le asignamos el tipo de letra
        self.login.setFont(self.letra2)
        # Le ponemos color de fondo, color de texto y margenes al letrero
        self.login.setStyleSheet("background-color: #White; color: #0000FF; padding: 40px;")
        self.login.setFixedWidth(200)

        self.login.move(67, 120)

        # Hacemos el campo para ingresar el primer numero
        self.editLogin = QLineEdit(self)
        # Definimos el ancho del campo en 200px
        self.editLogin.setFixedWidth(200)
        self.editLogin.setStyleSheet("background-color: White")
        # Establecemos que solo se ingrese un numero maximo de 20 digitos
        self.editLogin.setMaxLength(20)

        self.editLogin.move(67, 160)

        # Hacemos el letrero
        self.contrasena = QLabel(self)
        # Le escribimos el texto
        self.contrasena.setText("Contraseña")
        # Le asignamos el tipo de letra
        self.contrasena.setFont(self.letra2)
        # Le ponemos color de fondo, color de texto y margenes al letrero
        self.contrasena.setStyleSheet("background-color: #White; color: #FFFFFF; padding: 40px;")
        self.contrasena.setFixedWidth(200)

        self.contrasena.move(67, 200)

        # Hacemos el campo para ingresar el primer numero
        self.editContraseña = QLineEdit(self)
        # Definimos el ancho del campo en 200px
        self.editContraseña.setFixedWidth(200)
        self.editContraseña.setStyleSheet("background-color: White")
        # Establecemos que solo se ingrese un numero maximo de 20 digitos
        self.editContraseña.setMaxLength(20)

        self.editContraseña.move(67, 240)

        # Hacemos el letrero
        self.hotmail = QLabel(self)
        # Le escribimos el texto
        self.hotmail.setText("Correo")
        # Le asignamos el tipo de letra
        self.hotmail.setFont(self.letra2)
        # Le ponemos color de fondo, color de texto y margenes al letrero
        self.hotmail.setStyleSheet("background-color: #White; color: #FFFFFF; padding: 40px;")
        self.hotmail.setFixedWidth(200)

        self.hotmail.move(67, 280)

        # Hacemos el campo para ingresar el primer numero
        self.lineHotmail = QLineEdit(self)
        # Definimos el ancho del campo en 200px
        self.lineHotmail.setStyleSheet("background-color: White")
        self.lineHotmail.setFixedWidth(200)
        # Establecemos que solo se ingrese un numero maximo de 20 digitos
        self.lineHotmail.setMaxLength(50)

        self.lineHotmail.move(67, 320)

        # Hacemos el letrero
        self.nombre = QLabel(self)
        # Le escribimos el texto
        self.nombre.setText("Nombre")
        # Le asignamos el tipo de letra
        self.nombre.setFont(self.letra2)
        # Le ponemos color de fondo, color de texto y margenes al letrero
        self.nombre.setStyleSheet("background-color: #White; color: #FFFFFF; padding: 40px;")
        self.nombre.setFixedWidth(200)

        self.nombre.move(67, 360)

        # Hacemos el campo para ingresar el primer numero
        self.lineNombre = QLineEdit(self)
        # Definimos el ancho del campo en 200px
        self.lineNombre.setFixedWidth(200)
        self.lineNombre.setStyleSheet("background-color: White")
        # Establecemos que solo se ingrese un numero maximo de 20 digitos
        self.lineNombre.setMaxLength(50)

        self.lineNombre.move(67, 400)

        # Hacemos el letrero
        self.tipoUsuario = QLabel(self)
        # Le escribimos el texto
        self.tipoUsuario.setText("Tipo de Usuario")
        # Le asignamos el tipo de letra
        self.tipoUsuario.setFont(self.letra2)
        # Le ponemos color de fondo, color de texto y margenes al letrero
        self.tipoUsuario.setStyleSheet("background-color: #White; color: #FFFFFF; padding: 40px;")
        self.tipoUsuario.setFixedWidth(200)

        self.tipoUsuario.move(67, 440)

        # Line edit para ingresar el tipo de usuario
        self.employee_type_line = QLineEdit(self)
        self.employee_type_line.setPlaceholderText("Ingrese su codigo")
        self.employee_type_line.setFixedWidth(200)
        self.employee_type_line.setMaxLength(4)
        self.employee_type_line.setStyleSheet("background-color:white")
        self.employee_type_line.move(67, 480)

        self.botonCalcular = QPushButton(self)
        self.botonCalcular.setText("registrarse")
        self.botonCalcular.setFont(self.letra3)
        self.botonCalcular.setFixedWidth(250)
        self.botonCalcular.setFixedHeight(40)
        self.botonCalcular.setStyleSheet("background-color: #50D4FA; color: #000000  ; padding: 40px;")
        self.botonCalcular.move(320, 550)
        self.botonCalcular.clicked.connect(self.guardar_datos)

        self.volverMenu = QPushButton(self)
        self.volverMenu.setText("Volver Menu")
        self.volverMenu.setFont(self.letra3)
        self.volverMenu.setFixedWidth(250)
        self.volverMenu.setFixedHeight(40)
        self.volverMenu.setStyleSheet("background-color: #50D4FA; color: #000000  ; padding: 30px")
        self.volverMenu.move(50, 550)
        self.volverMenu.clicked.connect(self.cerrar_ventana)

    def set_background_image(self, image_path):
        # Load the background image
        background_image = QPixmap(image_path).scaled(self.ancho, self.alto)

        # Create a QLabel for the background image
        background_label = QLabel(self)
        background_label.setPixmap(background_image)
        background_label.setGeometry(0, 0, self.ancho, self.alto)

        # Set the background image to be in the back of all other widgets
        background_label.lower()

    def cerrar_ventana(self):
        self.close()

    def guardar_datos(self):
        usuario = self.editLogin.text()
        contrasena = self.editContraseña.text()
        correo = self.lineHotmail.text()
        nombre = self.lineNombre.text()
        tipoUsuario = self.employee_type_line.text()  # Obtener el texto del QLineEdit

        # Verificar si el correo tiene un formato válido
        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            self.mostrar_mensaje("Advertencia", "Por favor, ingrese un correo válido.")
            return

        # Verificar el tipo de usuario
        tipos_usuario_permitidos = ["1234", "5412"]

        if tipoUsuario not in tipos_usuario_permitidos:
            self.mostrar_mensaje("Advertencia", "Tipo de usuario no permitido"
                                                "\ningrese un codigo valido.")
            return

        # Verificar que el campo de nombre contenga solo letras
        if not re.match(r"^[a-zA-Z\s]+$", nombre):
            self.mostrar_mensaje("Advertencia", "Por favor, ingrese un nombre válido (solo letras y espacios).")
            return

        if usuario and contrasena and correo and nombre and tipoUsuario:
            with open('registros.txt', 'a') as archivo:
                archivo.write(f"Usuario: {usuario}\n")
                archivo.write(f"Contraseña: {contrasena}\n")
                archivo.write(f"Correo: {correo}\n")
                archivo.write(f"Nombre: {nombre}\n")
                archivo.write(f"TipoUsuario: {tipoUsuario}\n")  # Guardar el tipo de usuario
                archivo.write("\n")
            self.limpiar_campos()
            self.mostrar_mensaje("Registro Exitoso", "Los datos se han registrado exitosamente.")
        else:
            self.mostrar_mensaje("Advertencia", "Por favor, complete todos los campos.")

    def mostrar_mensaje(self, titulo, mensaje):
        mensaje_box = QMessageBox()
        mensaje_box.setWindowTitle(titulo)
        mensaje_box.setText(mensaje)
        mensaje_box.setIcon(QMessageBox.Information)
        mensaje_box.exec_()

    def limpiar_campos(self):
        self.editLogin.clear()
        self.editContraseña.clear()
        self.lineHotmail.clear()
        self.lineNombre.clear()
        self.employee_type_line.clear()

if __name__ == '__main__':
    aplicacion1 = QApplication(sys.argv)
    v1 = registrar1()
    v1.show()
    sys.exit(aplicacion1.exec_())
