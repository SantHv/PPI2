import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QLabel, QDesktopWidget,
    QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QDialog, QTextEdit, QHBoxLayout, QScrollArea, QFrame, QWidget,
    QComboBox
)


class TareaWidget(QFrame):
    def __init__(self, detalles_tarea):
        super(TareaWidget, self).__init__()

        # Configurar el diseño vertical para el widget de tarea
        self.setLayout(QVBoxLayout())

        # Crear etiquetas para mostrar detalles de la tarea
        etiqueta_tarea = QLabel(f"Tarea: {detalles_tarea['Tarea']}")
        etiqueta_tarea.setFont(QFont("Andale Mono", 14))

        etiqueta_observaciones = QLabel(f"Observaciones: {detalles_tarea['Observaciones']}")
        etiqueta_observaciones.setFont(QFont("Andale Mono", 14))

        # Obtener la ruta de la imagen de los detalles de la tarea
        ruta_imagen = detalles_tarea.get('Ruta de Imagen', '')

        # Si hay una ruta de imagen, intentar cargarla
        if ruta_imagen:
            print(f"Intentando cargar la imagen desde: {ruta_imagen}")
            imagen_label = QLabel()
            pixmap = QPixmap(ruta_imagen)
            if not pixmap.isNull():
                # Ajustar el ancho de la imagen y agregarla al diseño
                imagen_label.setPixmap(pixmap.scaledToWidth(300))
                self.layout().addWidget(imagen_label)

        # Agregar etiquetas al diseño
        self.layout().addWidget(etiqueta_tarea)
        self.layout().addWidget(etiqueta_observaciones)


class VentanaTareasCompletadas(QDialog):
    def __init__(self):
        super(VentanaTareasCompletadas, self).__init__()

        # Configurar la ventana de tareas completadas
        self.setWindowTitle("Tareas Completadas")
        self.setGeometry(100, 100, 800, 600)

        # Configurar el diseño principal de la ventana
        layout_principal = QVBoxLayout()

        # Configurar un área de desplazamiento para mostrar las tareas
        scroll_area = QScrollArea(self)
        contenido_widget = QWidget()
        contenido_layout = QVBoxLayout(contenido_widget)

        # Leer detalles de tareas completadas desde el archivo
        detalles_tareas_completadas = self.leer_tareas_desde_archivo("tareas_completadas.txt")

        # Crear un widget de tarea para cada conjunto de detalles
        for detalles_tarea in detalles_tareas_completadas:
            tarea_widget = TareaWidget(detalles_tarea)
            contenido_layout.addWidget(tarea_widget)

        # Configurar el área de desplazamiento con el contenido
        scroll_area.setWidget(contenido_widget)
        layout_principal.addWidget(scroll_area)

        # Configurar el diseño principal de la ventana
        self.setLayout(layout_principal)

    def leer_tareas_desde_archivo(self, archivo):
        detalles_tareas_completadas = []
        try:
            with open(archivo, "r") as file:
                lines = file.readlines()
                tarea = {}
                for line in lines:
                    if line.strip() == '---':
                        detalles_tareas_completadas.append(tarea)
                        tarea = {}
                    else:
                        key_value = line.strip().split(':')
                        if len(key_value) == 2:
                            key, value = key_value
                            tarea[key.strip()] = value.strip()
                        elif len(key_value) == 1 and key_value[0].strip():
                            tarea[key_value[0].strip()] = ''

                tarea['Hora de Tarea'] = tarea.get('Hora de Tarea', '00:00:00')

        except FileNotFoundError:
            print(f"El archivo {archivo} no existe.")

        return detalles_tareas_completadas


class EditarTareasVentana(QDialog):
    def __init__(self, contenido_inicial):
        super(EditarTareasVentana, self).__init__()

        # Configurar la ventana de edición de tareas
        self.setWindowTitle("Editar Tareas")
        self.setGeometry(100, 100, 800, 600)

        # Configurar el diseño vertical principal
        layout = QVBoxLayout()

        # Crear un editor de texto para editar el contenido
        self.editor_tareas = QTextEdit(self)
        self.editor_tareas.setPlainText(contenido_inicial)

        # Agregar el editor al diseño
        layout.addWidget(self.editor_tareas)

        # Crear un botón para guardar los cambios
        guardar_button = QPushButton("Guardar Cambios", self)
        guardar_button.clicked.connect(self.guardar_cambios)
        layout.addWidget(guardar_button)

        # Configurar el diseño de la ventana
        self.setLayout(layout)

    def guardar_cambios(self):
        # Guardar los cambios en el archivo
        contenido_editado = self.editor_tareas.toPlainText()
        nombre_archivo = "detalles_tarea.txt"

        try:
            with open(nombre_archivo, "w") as archivo:
                archivo.write(contenido_editado)
            QMessageBox.information(self, "Cambios Guardados", "Los cambios han sido guardados.")
        except Exception as e:
            QMessageBox.warning(self, "Error al Guardar Cambios",
                                f"No se pudieron guardar los cambios. Error: {str(e)}")


class Login5(QMainWindow):
    def __init__(self):
        super(Login5, self).__init__()

        # Configurar la ventana de inicio de sesión
        self.setStyleSheet("background-color: #BBF2FD;")
        self.setWindowTitle("Inicio de sesión")

        self.ancho = 1300
        self.alto = 900
        self.resize(self.ancho, self.alto)

        # Centrar la ventana en la pantalla
        self.pantalla = self.frameGeometry()
        self.centro = QDesktopWidget().availableGeometry().center()
        self.pantalla.moveCenter(self.centro)
        self.move(self.pantalla.topLeft())

        # Establecer un tamaño fijo para la ventana
        self.setFixedWidth(self.ancho)
        self.setFixedHeight(self.alto)

        # Fuente para letreros y botones
        fuente = QFont("Andale Mono", 18)

        # Crear elementos de la interfaz: etiquetas, campos de texto, botones, etc.
        self.etiqueta_titulo = QLabel("Tareas Diarias", self)
        self.etiqueta_titulo.move(550, 40)
        self.etiqueta_titulo.setFont(fuente)
        self.etiqueta_titulo.setFixedWidth(200)

        self.etiqueta_tarea = QLabel("Tarea", self)
        self.etiqueta_tarea.move(150, 120)
        self.etiqueta_tarea.setFont(fuente)
        self.editar_tarea = QLineEdit(self)
        self.editar_tarea.move(150, 170)
        self.editar_tarea.setFixedWidth(200)

        self.etiqueta_observaciones = QLabel("Observaciones", self)
        self.etiqueta_observaciones.move(450, 120)
        self.etiqueta_observaciones.setFixedWidth(200)
        self.etiqueta_observaciones.setFont(fuente)
        self.editar_observaciones = QTextEdit(self)
        self.editar_observaciones.move(450, 170)
        self.editar_observaciones.setFixedWidth(250)
        self.editar_observaciones.setFixedHeight(300)
        self.editar_observaciones.setAlignment(QtCore.Qt.AlignTop)

        self.etiqueta_hora = QLabel("Hora de Tarea", self)
        self.etiqueta_hora.move(750, 120)
        self.etiqueta_hora.setFont(fuente)
        self.etiqueta_hora.setFixedWidth(200)

        self.combo_horas = QComboBox(self)
        self.combo_horas.move(750, 170)
        self.combo_horas.setFixedWidth(200)
        horas = ["6:00 a 8:00 AM", "8:00 a 10:00 AM", "10:00 AM a 12:00 PM", "12:00 PM a 2:00 PM",
                 "2:00 PM a 4:00 PM", "4:00 PM a 6:00 PM"]
        self.combo_horas.addItems(horas)
        self.combo_horas.setCurrentIndex(0)

        self.boton_tareas_completadas = QPushButton("Tareas Completadas", self)
        self.boton_tareas_completadas.move(400, 700)
        self.boton_tareas_completadas.clicked.connect(self.mostrar_ventana_tareas_completadas)
        self.boton_tareas_completadas.setFixedWidth(200)
        self.boton_tareas_completadas.setStyleSheet("background-color: #50D4FA;")

        self.boton_enviar = QPushButton("Enviar Tarea", self)
        self.boton_enviar.move(150, 700)
        self.boton_enviar.clicked.connect(self.enviar_detalles_tarea)
        self.boton_enviar.setFixedWidth(200)
        self.boton_enviar.setStyleSheet("background-color: #50D4FA;")

        self.boton_eliminar_tareas = QPushButton("Eliminar Todas las Tareas", self)
        self.boton_eliminar_tareas.move(650, 700)
        self.boton_eliminar_tareas.clicked.connect(self.eliminar_todas_las_tareas)
        self.boton_eliminar_tareas.setFixedWidth(200)
        self.boton_eliminar_tareas.setStyleSheet("background-color: #50D4FA;")

        self.boton_editar_archivo = QPushButton("Editar Tareas", self)
        self.boton_editar_archivo.move(900, 700)
        self.boton_editar_archivo.clicked.connect(self.abrir_ventana_editar_archivo)
        self.boton_editar_archivo.setFixedWidth(200)
        self.boton_editar_archivo.setStyleSheet("background-color: #50D4FA;")

        self.editar_tarea.setStyleSheet("background-color: white; border: 1px solid black;")
        self.editar_observaciones.setStyleSheet("background-color: white; border: 1px solid black;")

    def enviar_detalles_tarea(self):
        tarea = self.editar_tarea.text()
        observaciones = self.editar_observaciones.toPlainText()
        hora = self.combo_horas.currentText()

        if not tarea or not observaciones or not hora:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor, complete todos los campos.")
            return

        detalles_tarea = f"Tarea: {tarea}\nObservaciones: {observaciones}\nHora de Tarea: {hora}\n"
        detalles_tarea += "\n---\n"

        nombre_archivo = "detalles_tarea.txt"
        with open(nombre_archivo, "a") as archivo:
            archivo.write(detalles_tarea)

        QMessageBox.information(self, "Envío Exitoso", "Los detalles de la tarea se han enviado con éxito.")
        self.limpiar_campos()

    def mostrar_ventana_tareas_completadas(self):
        try:
            ventana_tareas_completadas = VentanaTareasCompletadas()
            ventana_tareas_completadas.exec_()
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error al abrir la ventana de tareas completadas: {str(e)}")

    def limpiar_campos(self):
        self.editar_tarea.clear()
        self.editar_observaciones.clear()

    def eliminar_todas_las_tareas(self):
        try:
            nombre_archivo = "detalles_tarea.txt"
            with open(nombre_archivo, "w") as archivo:
                archivo.write("")
            QMessageBox.information(self, "Tareas Eliminadas", "Se han eliminado todas las tareas.")
        except Exception as e:
            QMessageBox.warning(self, "Error al Eliminar Tareas",
                                f"No se pudieron eliminar las tareas. Error: {str(e)}")

    def abrir_ventana_editar_archivo(self):
        try:
            nombre_archivo = "detalles_tarea.txt"
            with open(nombre_archivo, "r") as archivo:
                contenido = archivo.read()

            ventana_editar = EditarTareasVentana(contenido)
            ventana_editar.exec_()
        except Exception as e:
            QMessageBox.warning(self, "Error al Abrir Archivo", f"No se pudo abrir el archivo. Error: {str(e)}")


if __name__ == '__main__':
    aplicacion1 = QApplication(sys.argv)
    v1 = Login5()
    v1.show()
    aplicacion1.exec_()
