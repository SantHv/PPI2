import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QLabel, QDesktopWidget,
    QVBoxLayout, QWidget, QScrollArea, QStackedWidget,
    QPushButton
)

class ImagenLabel(QLabel):
    def __init__(self, ruta_imagen):
        super(ImagenLabel, self).__init__()
        pixmap = QtGui.QPixmap(ruta_imagen)
        if not pixmap.isNull():
            # Establecer un tamaño máximo para las imágenes
            max_width = 1000
            max_height = 700

            pixmap = pixmap.scaled(max_width, max_height, QtCore.Qt.KeepAspectRatio)
            self.setPixmap(pixmap)
            self.setScaledContents(True)

class VentanaTareasCompletadas(QMainWindow):
    def __init__(self):
        super(VentanaTareasCompletadas, self).__init__()

        self.setWindowTitle("Tareas Completadas")
        self.setWindowIcon(QtGui.QIcon("imagenes/icono1.png"))

        self.ancho = 1200
        self.alto = 800
        self.resize(self.ancho, self.alto)

        self.pantalla = self.frameGeometry()
        self.centro = QDesktopWidget().availableGeometry().center()
        self.pantalla.moveCenter(self.centro)
        self.move(self.pantalla.topLeft())

        # Crear un área de desplazamiento para las tareas completadas
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Crear un widget para contener las tareas completadas
        widget_tareas_completadas = QWidget(self)
        widget_tareas_completadas_layout = QVBoxLayout(widget_tareas_completadas)

        # Leer tareas desde el archivo (ajusta según el formato real de tu archivo)
        self.detalles_tareas_completadas = self.leer_tareas_desde_archivo("tareas_completadas.txt")

        # Crear un widget apilado para mostrar una tarea a la vez
        self.stacked_widget = QStackedWidget(self)

        # Agregar todas las tareas al widget apilado
        for detalles_tarea in self.detalles_tareas_completadas:
            widget_tarea = QWidget(self)
            widget_tarea_layout = QVBoxLayout(widget_tarea)

            etiqueta_tarea = QLabel(f"Tarea: {detalles_tarea['Tarea']}", self)
            etiqueta_tarea.setFont(QtGui.QFont("Andale Mono", 14))

            etiqueta_observaciones = QLabel(f"Observaciones: {detalles_tarea['Observaciones']}", self)
            etiqueta_observaciones.setFont(QtGui.QFont("Andale Mono", 14))

            # Verificar si hay una ruta de imagen y cargarla
            ruta_imagen = detalles_tarea.get('Ruta de Imagen', '')
            if ruta_imagen:
                print(f"Intentando cargar la imagen desde: {ruta_imagen}")
                imagen_label = ImagenLabel(ruta_imagen)
                widget_tarea_layout.addWidget(imagen_label)

            widget_tarea_layout.addWidget(etiqueta_tarea)
            widget_tarea_layout.addWidget(etiqueta_observaciones)

            # Agregar el widget de tarea al widget apilado
            self.stacked_widget.addWidget(widget_tarea)

        # Agregar el widget apilado al layout principal
        widget_tareas_completadas_layout.addWidget(self.stacked_widget)

        scroll_area.setWidget(widget_tareas_completadas)

        # Agregar el área de desplazamiento a la ventana
        self.setCentralWidget(scroll_area)

        # Crear botones de navegación
        btn_anterior = QPushButton("Anterior", self)
        btn_anterior.clicked.connect(self.mostrar_tarea_anterior)

        btn_siguiente = QPushButton("Siguiente", self)
        btn_siguiente.clicked.connect(self.mostrar_tarea_siguiente)

        # Agregar los botones al layout principal
        widget_tareas_completadas_layout.addWidget(btn_anterior)
        widget_tareas_completadas_layout.addWidget(btn_siguiente)

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

    def mostrar_tarea_anterior(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index > 0:
            self.stacked_widget.setCurrentIndex(current_index - 1)

    def mostrar_tarea_siguiente(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index < len(self.detalles_tareas_completadas) - 1:
            self.stacked_widget.setCurrentIndex(current_index + 1)


if __name__ == '__main__':
    aplicacion1 = QApplication(sys.argv)
    v1 = VentanaTareasCompletadas()
    v1.show()
    aplicacion1.exec_()
