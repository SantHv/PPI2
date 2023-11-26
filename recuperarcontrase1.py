import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QDesktopWidget
from PyQt5.QtGui import QFont


class RecuperarContrasenaVentana(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Recuperar Contraseña')
        self.setStyleSheet("background-color: #BBFDF8;")

        # Elementos de la interfaz
        self.label_correo = QLabel('Ingrese su correo:')
        self.label_correo.setFixedWidth(200)
        self.label_correo.setFixedHeight(100)

        # Aumentar el tamaño de la letra del QLabel
        font = QFont()
        font.setPointSize(14)  # Ajusta el tamaño según tus preferencias
        self.label_correo.setFont(font)

        self.entry_correo = QLineEdit()
        self.button_recuperar = QPushButton('Recuperar Contraseña')

        # Establecer el color blanco para QLineEdit y QPushButton
        self.entry_correo.setStyleSheet("background-color: white;")
        self.button_recuperar.setStyleSheet("background-color: #50D4FA; color: #000000;")

        self.label_resultado = QLabel('')

        # Diseño de la interfaz
        layout = QVBoxLayout()
        layout.addWidget(self.label_correo)
        layout.addWidget(self.entry_correo)
        layout.addWidget(self.button_recuperar)
        layout.addWidget(self.label_resultado)

        self.setLayout(layout)

        # Conectar el botón a la función recuperar_contrasena
        self.button_recuperar.clicked.connect(self.recuperar_contrasena)

        # Ajustar tamaño de la ventana
        self.resize(300, 200)

        # Centrar la ventana en la pantalla
        self.center()

    def center(self):
        # Obtener la geometría de la pantalla
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()

        # Centrar la geometría de la ventana en el centro de la pantalla
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def recuperar_contrasena(self):
        correo_buscar = self.entry_correo.text()

        try:
            with open('registros.txt', 'r') as file:
                registros = file.read().split('\n\n')

                for registro in registros:
                    if f'Correo: {correo_buscar}' in registro:
                        # Buscar la contraseña en el registro
                        lineas = registro.split('\n')
                        for linea in lineas:
                            if linea.startswith('Contraseña:'):
                                contrasena = linea.split(': ')[1]
                                self.label_resultado.setText(f'Contraseña: {contrasena}')
                                return

                # Si el correo no se encuentra
                self.label_resultado.setText('Correo no encontrado')

        except FileNotFoundError:
            self.label_resultado.setText('Archivo no encontrado')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = RecuperarContrasenaVentana()
    ventana.show()
    sys.exit(app.exec_())
