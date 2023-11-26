import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QLabel, QDesktopWidget,
    QLineEdit, QPushButton, QCheckBox, QMessageBox
)

class Login5(QMainWindow):
    def __init__(self):
        super(Login5, self).__init__()

        self.setWindowTitle("Inicio de sesión")
        self.setWindowIcon(QtGui.QIcon("imagenes/icono1.png"))

        self.ancho = 1200
        self.alto = 800
        self.resize(self.ancho, self.alto)

        self.pantalla = self.frameGeometry()
        self.centro = QDesktopWidget().availableGeometry().center()
        self.pantalla.moveCenter(self.centro)
        self.move(self.pantalla.topLeft())

        self.setFixedWidth(self.ancho)
        self.setFixedHeight(self.alto)

        # Fuente para letreros y botones
        fuente = QFont("Andale Mono", 18)

        # Tarea
        self.etiqueta_tarea = QLabel("Tarea", self)
        self.etiqueta_tarea.move(150, 80)
        self.etiqueta_tarea.setFont(fuente)
        self.editar_tarea = QLineEdit(self)
        self.editar_tarea.move(120, 150)

        # Observaciones
        self.etiqueta_observaciones = QLabel("Observaciones", self)
        self.etiqueta_observaciones.move(350, 80)
        self.etiqueta_observaciones.setFixedWidth(200)
        self.etiqueta_observaciones.setFont(fuente)
        self.editar_observaciones = QLineEdit(self)
        self.editar_observaciones.move(350, 150)
        self.editar_observaciones.setFixedWidth(210)
        self.editar_observaciones.setFixedHeight(300)

        # Imagen con apariencia clara
        self.etiqueta_imagen = QLabel(self)
        self.etiqueta_imagen.setGeometry(700, 150, 300, 300)
        self.etiqueta_imagen.setStyleSheet("QLabel { background-color : rgba(255, 255, 255, 150); }")  # Ajustar la opacidad

        # Botón para enviar los detalles de la tarea al empleado
        self.boton_enviar = QPushButton("Enviar Tarea", self)
        self.boton_enviar.move(1000, 250)

        # Conectar el botón de enviar a la función de enviar detalles de tarea
        self.boton_enviar.clicked.connect(self.enviar_detalles_tarea)

    def enviar_detalles_tarea(self):
        tarea = self.editar_tarea.text()
        observaciones = self.editar_observaciones.text()

        # Validar que la tarea y las observaciones no estén vacías
        if not tarea or not observaciones:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, complete todos los campos.")
            return

        # Crear una cadena con los detalles de la tarea
        detalles_tarea = f"Tarea: {tarea}\nObservaciones: {observaciones}\n"

        # Agregar una línea de guiones como separador
        detalles_tarea += "\n---\n"

        # Guardar los detalles en un archivo de texto
        nombre_archivo = "detalles_tarea.txt"
        with open(nombre_archivo, "a") as archivo:
            archivo.write(detalles_tarea)

        # Mostrar un mensaje de éxito
        QMessageBox.information(self, "Envío Exitoso", "Los detalles de la tarea se han enviado con éxito.")

# Bloque principal
if __name__ == '__main__':
    aplicacion1 = QApplication(sys.argv)
    v1 = Login5()
    v1.show()
    sys.exit(aplicacion1.exec_())
