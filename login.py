import os
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QVBoxLayout, QLabel, QLineEdit, QApplication, QPushButton, \
    QMainWindow, QMessageBox, QCheckBox, QComboBox

from registrar import registrar1
from main import TareasEmpleada
from ventana2 import Login5


class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()

        self.setWindowTitle("Inicio de sesión")
        self.setWindowIcon(QtGui.QIcon("imagenes/icono1.png"))

        self.ancho = 900
        self.alto = 600
        self.resize(self.ancho, self.alto)

        self.pantalla = self.frameGeometry()
        self.centro = QDesktopWidget().availableGeometry().center()
        self.pantalla.moveCenter(self.centro)
        self.move(self.pantalla.topLeft())

        self.setFixedWidth(self.ancho)
        self.setFixedHeight(self.alto)

        self.set_background_image("imagenes/fnd1.png")

        self.letra1 = QtGui.QFont()
        self.letra1.setFamily("Andale mono")
        self.letra1.setPointSize(18)

        self.logo_label = QLabel(self)
        pixmap = QPixmap("imagenes/DOM1.png")
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setFixedSize(pixmap.size())
        self.logo_label.move(485, 220)

        self.letra2 = QtGui.QFont()
        self.letra2.setFamily("Andale mono")
        self.letra2.setPointSize(16)

        self.letrero1 = QLabel(self)
        self.letrero1.setText("Domestic Space")
        self.letrero1.setFont(self.letra1)
        self.letrero1.setStyleSheet("background-color:color: #09B4AC; padding: 50px;")
        self.letrero1.setFixedWidth(500)
        self.letrero1.move(340, 50)

        self.login = QLabel(self)
        self.login.setText("Usuario")
        self.login.setFont(self.letra1)
        self.login.setStyleSheet("background-color: #White; color: #0000FF; padding: 40px;")
        self.login.setFixedWidth(250)
        self.login.move(305, 120)

        self.editLogin = QLineEdit(self)
        self.editLogin.setFixedWidth(250)
        self.editLogin.setMaxLength(20)
        self.editLogin.setStyleSheet("background-color: white")
        self.editLogin.move(305, 160)

        self.contraseña = QLabel(self)
        self.contraseña.setText("Contraseña")
        self.contraseña.setFont(self.letra1)
        self.contraseña.setStyleSheet("background-color: #White; color: #FFFFFF; padding: 40px;")
        self.contraseña.setFixedWidth(200)
        self.contraseña.move(305, 200)

        self.editContraseña = QLineEdit(self)
        self.editContraseña.setFixedWidth(250)
        self.editContraseña.setStyleSheet("background-color: white")
        self.editContraseña.setMaxLength(20)
        self.editContraseña.setEchoMode(QLineEdit.Password)
        self.editContraseña.move(305, 240)

        self.tipoUsuario = QLabel(self)
        self.tipoUsuario.setText("Tipo de Usuario")
        self.tipoUsuario.setFont(self.letra1)
        self.tipoUsuario.setStyleSheet("background-color: #White; color: #FFFFFF; padding: 40px;")
        self.tipoUsuario.setFixedWidth(250)
        self.tipoUsuario.move(305, 280)

        self.user_type_line = QLineEdit(self)
        self.user_type_line.setPlaceholderText("Ingrese su código")
        self.user_type_line.setFixedWidth(250)
        self.user_type_line.setStyleSheet("background-color: white")
        self.user_type_line.move(305, 320)

        self.botonCalcular = QPushButton(self)
        self.botonCalcular.setText("Iniciar Sesión")
        self.botonCalcular.setFixedWidth(200)
        self.botonCalcular.setStyleSheet("background-color: #50D4FA; color: #000000  ; padding: 30px;font-weight: bold;")
        self.botonCalcular.move(325, 450)
        self.botonCalcular.setFixedHeight(40)

        self.botonRegistrar = QPushButton(self)
        self.botonRegistrar.setText("Registrarse")
        self.botonRegistrar.setFixedWidth(200)
        self.botonRegistrar.setStyleSheet("background-color: #50D4FA; color: #000000  ; padding: 30px;font-weight: bold;")
        self.botonRegistrar.move(325, 500)
        self.botonRegistrar.setFixedHeight(40)

        self.mostrar_contraseña_checkbox = QCheckBox("Mostrar Contraseña", self)
        self.mostrar_contraseña_checkbox.setStyleSheet("font-weight: bold;")
        self.mostrar_contraseña_checkbox.move(570, 240)
        self.mostrar_contraseña_checkbox.setFixedWidth(200)
        self.mostrar_contraseña_checkbox.stateChanged.connect(self.toggle_password_visibility)

        self.botonCalcular.clicked.connect(self.check_login)
        self.botonRegistrar.clicked.connect(self.abrir_registrar)

        self.login5_instance = None  # Nuevo atributo para almacenar la instancia de Login5

    def set_background_image(self, image_path):
        background_image = QtGui.QPixmap(image_path).scaled(self.ancho, self.alto)
        background_label = QLabel(self)
        background_label.setPixmap(background_image)
        background_label.setGeometry(0, 0, self.ancho, self.alto)
        background_label.lower()

    def check_login(self):
        username = self.editLogin.text()
        password = self.editContraseña.text()
        tipo_usuario = self.user_type_line.text()

        script_dir = os.path.dirname(os.path.abspath(__file__))
        registros_file = os.path.join(script_dir, 'registros.txt')

        try:
            with open('registros.txt', 'r') as archivo:
                lineas = archivo.readlines()

            usuarios = []
            usuario_actual = {}
            for linea in lineas:
                linea = linea.strip()
                if linea:
                    clave, valor = linea.split(': ')
                    usuario_actual[clave] = valor
                else:
                    usuarios.append(usuario_actual)
                    usuario_actual = {}

            for usuario in usuarios:
                if (
                        usuario.get("Usuario") == username and
                        usuario.get("Contraseña") == password and
                        usuario.get("TipoUsuario") == tipo_usuario
                ):
                    if tipo_usuario == "1234":
                        self.login5_instance = Login5()
                        self.login5_instance.destroyed.connect(self.show_login)
                        self.login5_instance.show()
                        self.close()
                    elif tipo_usuario == "5412":
                        ventana = TareasEmpleada()
                        ventana.show()
                        self.close()
                    else:
                        QMessageBox.warning(self, 'Error', 'Tipo de usuario no reconocido.')
                    break
            else:
                QMessageBox.warning(self, 'Error', 'Credenciales incorrectas.')
        except FileNotFoundError:
            QMessageBox.warning(self, 'Error', 'No se encontró el archivo "registros.txt".')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error inesperado: {str(e)}')

    def show_login(self):
        # Este método se ejecuta cuando la instancia de Login5 se destruye
        self.show()

    def abrir_registrar(self):
        self.boton_Registrar = registrar1()
        self.boton_Registrar.show()

    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            self.editContraseña.setEchoMode(QLineEdit.Normal)
        else:
            self.editContraseña.setEchoMode(QLineEdit.Password)

if __name__ == '__main__':
    aplicacion1 = QApplication(sys.argv)
    v1 = Login()
    v1.show()
    sys.exit(aplicacion1.exec_())
