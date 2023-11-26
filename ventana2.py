import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QLabel, QDesktopWidget,
    QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QDialog, QTextEdit, QHBoxLayout, QScrollArea, QFrame, QWidget
)


class TareaWidget(QFrame):
    def __init__(self, detalles_tarea):
        super(TareaWidget, self).__init__()

        self.setLayout(QVBoxLayout())

        etiqueta_tarea = QLabel(f"Tarea: {detalles_tarea['Tarea']}")
        etiqueta_tarea.setFont(QFont("Andale Mono", 14))

        etiqueta_observaciones = QLabel(f"Observaciones: {detalles_tarea['Observaciones']}")
        etiqueta_observaciones.setFont(QFont("Andale Mono", 14))

        ruta_imagen = detalles_tarea.get('Ruta de Imagen', '')
        if ruta_imagen:
            print(f"Intentando cargar la imagen desde: {ruta_imagen}")
            imagen_label = QLabel()
            pixmap = QPixmap(ruta_imagen)
            if not pixmap.isNull():
                imagen_label.setPixmap(pixmap.scaledToWidth(300))  # Ajusta el ancho según sea necesario
                self.layout().addWidget(imagen_label)

        self.layout().addWidget(etiqueta_tarea)
        self.layout().addWidget(etiqueta_observaciones)

class VentanaTareasCompletadas(QDialog):
    def __init__(self):
        super(VentanaTareasCompletadas, self).__init__()

        self.setWindowTitle("Tareas Completadas")
        self.setGeometry(100, 100, 800, 600)

        layout_principal = QVBoxLayout()

        scroll_area = QScrollArea(self)
        contenido_widget = QWidget()
        contenido_layout = QVBoxLayout(contenido_widget)

        detalles_tareas_completadas = self.leer_tareas_desde_archivo("tareas_completadas.txt")

        for detalles_tarea in detalles_tareas_completadas:
            tarea_widget = TareaWidget(detalles_tarea)
            contenido_layout.addWidget(tarea_widget)

        scroll_area.setWidget(contenido_widget)
        layout_principal.addWidget(scroll_area)

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

        self.setWindowTitle("Editar Tareas")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.editor_tareas = QTextEdit(self)
        self.editor_tareas.setPlainText(contenido_inicial)

        layout.addWidget(self.editor_tareas)

        guardar_button = QPushButton("Guardar Cambios", self)
        guardar_button.clicked.connect(self.guardar_cambios)
        layout.addWidget(guardar_button)

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
            QMessageBox.warning(self, "Error al Guardar Cambios", f"No se pudieron guardar los cambios. Error: {str(e)}")

class Login5(QMainWindow):
    def __init__(self):
        super(Login5, self).__init__()

        self.setWindowTitle("Inicio de sesión")

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
        self.editar_tarea.move(150, 150)
        self.editar_tarea.setFixedWidth(200)

        # Observaciones
        self.etiqueta_observaciones = QLabel("Observaciones", self)
        self.etiqueta_observaciones.move(450, 80)
        self.etiqueta_observaciones.setFixedWidth(200)
        self.etiqueta_observaciones.setFont(fuente)
        self.editar_observaciones = QTextEdit(self)
        self.editar_observaciones.move(450, 150)
        self.editar_observaciones.setFixedWidth(210)
        self.editar_observaciones.setFixedHeight(300)

        # Configurar el cursor para comenzar desde la parte superior
        self.editar_observaciones.setAlignment(QtCore.Qt.AlignTop)

        # Botón para Tareas Completadas
        self.boton_tareas_completadas = QPushButton("Tareas Completadas", self)
        self.boton_tareas_completadas.move(800, 300)
        self.boton_tareas_completadas.clicked.connect(self.mostrar_ventana_tareas_completadas)
        self.boton_tareas_completadas.setFixedWidth(200)

        # Botón para enviar los detalles de la tarea al empleado
        self.boton_enviar = QPushButton("Enviar Tarea", self)
        self.boton_enviar.move(800, 250)
        self.boton_enviar.clicked.connect(self.enviar_detalles_tarea)
        self.boton_enviar.setFixedWidth(200)

        # Botón para eliminar todas las tareas
        self.boton_eliminar_tareas = QPushButton("Eliminar Todas las Tareas", self)
        self.boton_eliminar_tareas.move(800, 350)
        self.boton_eliminar_tareas.clicked.connect(self.eliminar_todas_las_tareas)
        self.boton_eliminar_tareas.setFixedWidth(200)

        # Botón para editar el archivo
        self.boton_editar_archivo = QPushButton("Editar Archivo", self)
        self.boton_editar_archivo.move(800, 400)
        self.boton_editar_archivo.clicked.connect(self.abrir_ventana_editar_archivo)
        self.boton_editar_archivo.setFixedWidth(200)

        self.setStyleSheet("background-color: lightgray;")
        self.editar_tarea.setStyleSheet("background-color: white; border: 1px solid black;")
        self.editar_observaciones.setStyleSheet("background-color: white; border: 1px solid black;")

    def enviar_detalles_tarea(self):
        tarea = self.editar_tarea.text()
        observaciones = self.editar_observaciones.toPlainText()

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

        # Limpiar los campos después de enviar la tarea
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
            QMessageBox.warning(self, "Error al Eliminar Tareas", f"No se pudieron eliminar las tareas. Error: {str(e)}")

    def abrir_ventana_editar_archivo(self):
        try:
            nombre_archivo = "detalles_tarea.txt"
            with open(nombre_archivo, "r") as archivo:
                contenido = archivo.read()

            ventana_editar = EditarTareasVentana(contenido)
            ventana_editar.exec_()  # Cambiar exec() a exec_()
        except Exception as e:
            QMessageBox.warning(self, "Error al Abrir Archivo", f"No se pudo abrir el archivo. Error: {str(e)}")


if __name__ == '__main__':
    aplicacion1 = QApplication(sys.argv)
    v1 = Login5()
    v1.show()
    aplicacion1.exec_()
