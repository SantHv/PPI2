import sys
import os
import shutil
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QLabel, QDesktopWidget,
    QLineEdit, QPushButton, QCheckBox, QFileDialog, QTextEdit,
    QVBoxLayout, QWidget, QHBoxLayout, QScrollArea, QMessageBox
)


class TareasEmpleada(QMainWindow):
    def __init__(self):
        super(TareasEmpleada, self).__init__()
        self.setStyleSheet("background-color: #BBF2FD;")
        self.setWindowTitle("Tareas Diarias - Empleada Doméstica")
        self.setWindowIcon(QtGui.QIcon("imagenes/icono1.png"))

        self.ancho = 1400
        self.alto = 900
        self.resize(self.ancho, self.alto)

        self.pantalla = self.frameGeometry()
        self.centro = QDesktopWidget().availableGeometry().center()
        self.pantalla.moveCenter(self.centro)
        self.move(self.pantalla.topLeft())

        # Desactivar el ajuste automático del tamaño de la ventana
        self.setFixedSize(self.size())

        # Fuente para letreros y botones
        self.fuente = QFont("Andale Mono", 14)

        # Layout principal
        layout_principal = QVBoxLayout()

        # Agregar título "Tareas"
        titulo_tareas = QLabel("Tareas", self)
        titulo_tareas.setFont(QFont("Andale Mono", 18, QtGui.QFont.Bold))
        layout_principal.addWidget(titulo_tareas, alignment=QtCore.Qt.AlignCenter)

        # Widget contenedor para tareas
        self.widget_tareas = QWidget(self)
        self.widget_tareas_layout = QVBoxLayout(self.widget_tareas)

        # Wrap the widget_tareas in a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.widget_tareas)

        # Campos para mostrar hasta 5 tareas
        self.campos_tareas = []

        for i in range(3):
            self.agregar_nueva_tarea()

        # Añadir el widget de tareas al layout principal
        layout_principal.addWidget(scroll_area)

        # Agregar el layout principal al widget central
        widget_central = QWidget(self)
        widget_central.setLayout(layout_principal)
        self.setCentralWidget(widget_central)

        # Leer detalles de la tarea desde el archivo
        self.mostrar_detalles_tarea()

    def subir_imagen(self, tarea_index):
        opciones = QFileDialog.Options()
        opciones |= QFileDialog.ReadOnly
        ruta_archivo, _ = QFileDialog.getOpenFileName(self, f"Seleccionar Imagen para Tarea {tarea_index + 1}", "",
                                                      "Image Files (*.png *.jpg *.bmp);;All Files (*)",
                                                      options=opciones)

        if ruta_archivo:
            # Crear un directorio para almacenar las imágenes si no existe
            directorio_imagenes = "imagenes_tareas"
            os.makedirs(directorio_imagenes, exist_ok=True)

            # Copiar la imagen al directorio
            nueva_ruta = os.path.join(directorio_imagenes, f"imagen_tarea_{tarea_index + 1}{os.path.splitext(ruta_archivo)[1]}")
            shutil.copyfile(ruta_archivo, nueva_ruta)

            # Guardar la nueva ruta de la imagen en la lista
            self.campos_tareas[tarea_index]['Ruta Imagen'] = nueva_ruta
            print(f"Imagen para Tarea {tarea_index + 1}: {nueva_ruta}")

    def enviar_tarea(self, tarea_index):
        # Verificar si el checkbox está marcado
        if self.campos_tareas[tarea_index]['Checkbox Completado'].isChecked():
            # Obtener detalles de la tarea
            tarea = self.campos_tareas[tarea_index]['Editar Tarea'].text()
            observaciones = self.campos_tareas[tarea_index]['Editar Observaciones'].toPlainText()
            ruta_imagen = self.campos_tareas[tarea_index]['Ruta Imagen']
            hora_tarea = self.campos_tareas[tarea_index]['Hora Tarea'].text()

            # Validaciones
            if not tarea or not observaciones:
                QMessageBox.critical(self, "Error", "Complete todos los campos antes de enviar la tarea.")
                return

            # Crear una cadena con los detalles de la tarea
            detalles_tarea = f"Tarea: {tarea}\nObservaciones: {observaciones}"

            if ruta_imagen:
                detalles_tarea += f"\nRuta de Imagen: {ruta_imagen}"

            detalles_tarea += f"\nHora de Tarea: {hora_tarea}"  # Agregar la hora

            # Agregar una línea de guiones como separador
            detalles_tarea += "\n---\n"

            # Guardar los detalles en el archivo tareas_completadas.txt
            with open("tareas_completadas.txt", "a") as archivo:
                archivo.write(detalles_tarea)

            QMessageBox.information(self, "Éxito", f"Tarea {tarea_index + 1} Enviada y guardada.")
            print(f"Tarea {tarea_index + 1} enviada y guardada en tareas_completadas.txt.")
        else:
            QMessageBox.warning(self, "Error", f"Marque la casilla de verificación para completar la tarea {tarea_index + 1}.")

    # ...

    def mostrar_detalles_tarea(self):
        # Leer detalles de la tarea desde el archivo
        try:
            with open("detalles_tarea.txt", "r") as archivo:
                contenido = archivo.read()

            tareas = contenido.split("---")[:-1]  # Dividir por "---" y excluir la última parte vacía

            # Asegurar que haya suficientes elementos en self.campos_tareas
            while len(self.campos_tareas) < len(tareas):
                self.agregar_nueva_tarea()

            # Recorrer cada tarea
            for i, tarea in enumerate(tareas):
                # Limpiar espacios al principio y al final de cada línea
                detalles_tarea = [linea.strip() for linea in tarea.strip().split('\n')]

                tarea_texto = detalles_tarea[0].split(":")[1].strip()
                observaciones = detalles_tarea[1].split(":")[1].strip()
                hora_tarea = ':'.join(detalles_tarea[2:])  # Unir todas las partes restantes

                # Mostrar detalles en la interfaz
                self.campos_tareas[i]['Editar Tarea'].setText(tarea_texto)
                self.campos_tareas[i]['Editar Observaciones'].setText(observaciones)
                self.campos_tareas[i]['Hora Tarea'].setText(hora_tarea)

        except FileNotFoundError:
            print("El archivo detalles_tarea.txt no existe.")

    # ...

    def agregar_nueva_tarea(self):
        # Agregar una nueva tarea al final de la lista campos_tareas
        i = len(self.campos_tareas)
        tarea_layout = self.crear_tarea_layout(i)
        self.widget_tareas_layout.addLayout(tarea_layout)
        self.campos_tareas.append({
            'Editar Tarea': tarea_layout.itemAt(1).widget(),
            'Editar Observaciones': tarea_layout.itemAt(3).widget(),
            'Checkbox Completado': tarea_layout.itemAt(4).widget(),
            'Boton Subir Imagen': tarea_layout.itemAt(5).widget(),
            'Boton Enviar': tarea_layout.itemAt(6).widget(),
            'Ruta Imagen': '',
            'Hora Tarea': tarea_layout.itemAt(7).widget(),  # Agregar el nuevo campo de hora
        })

    # ...

    def crear_tarea_layout(self, index):
        tarea_layout = QHBoxLayout()

        etiqueta_tarea = QLabel(f"Tarea {index + 1}", self)
        etiqueta_tarea.setFont(self.fuente)

        editar_tarea = QLineEdit(self)
        editar_tarea.setReadOnly(True)
        editar_tarea.setFixedSize(180, 40)
        editar_tarea.setStyleSheet("background-color: white;")  # Fondo blanco

        etiqueta_observaciones = QLabel(f"Detalles {index + 1}", self)
        etiqueta_observaciones.setFont(self.fuente)
        etiqueta_observaciones.setFixedWidth(200)

        editar_observaciones = QTextEdit(self)
        editar_observaciones.setFixedSize(200, 100)
        editar_observaciones.setStyleSheet("background-color: white;")  # Fondo blanco
        editar_observaciones.setAlignment(QtCore.Qt.AlignTop)  # Alineación vertical superior
        editar_observaciones.setReadOnly(True)  # Permitir edición
        editar_observaciones.setWordWrapMode(
            QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)  # Activar ajuste automático de líneas

        checkbox_completado = QCheckBox(f"Tarea {index + 1} Completada", self)

        boton_subir_imagen = QPushButton(f"Subir Imagen {index + 1}", self)
        boton_subir_imagen.clicked.connect(lambda _, index=index: self.subir_imagen(index))
        boton_subir_imagen.setStyleSheet("background-color: #50D4FA;")

        # Nuevo botón "Enviar" para cada tarea
        boton_enviar = QPushButton(f"Enviar {index + 1}", self)
        boton_enviar.clicked.connect(lambda _, index=index: self.enviar_tarea(index))
        boton_enviar.setStyleSheet("background-color: #50D4FA;")  # Fondo blanco

        # Nuevo campo de hora (QLineEdit no editable)
        hora_tarea = QLineEdit(self)
        hora_tarea.setReadOnly(True)
        hora_tarea.setFixedSize(220, 40)
        hora_tarea.setStyleSheet("background-color: white;")  # Fondo blanco
        hora_tarea.setAlignment(QtCore.Qt.AlignCenter)  # Alinea el texto al centro

        tarea_layout.addWidget(etiqueta_tarea)
        tarea_layout.addWidget(editar_tarea)
        tarea_layout.addWidget(etiqueta_observaciones)
        tarea_layout.addWidget(editar_observaciones)
        tarea_layout.addWidget(checkbox_completado)
        tarea_layout.addWidget(boton_subir_imagen)
        tarea_layout.addWidget(boton_enviar)
        tarea_layout.addWidget(hora_tarea)  # Agrega el nuevo campo de hora

        # Modifica la disposición para que los elementos se expandan verticalmente
        tarea_layout.setStretch(1, 1)  # Hace que editar_tarea se expanda verticalmente
        tarea_layout.setStretch(3, 1)  # Hace que editar_observaciones se expanda verticalmente

        return tarea_layout

    # ...


# Bloque principal
if __name__ == '__main__':
    aplicacion = QApplication(sys.argv)
    ventana_tareas = TareasEmpleada()
    ventana_tareas.show()
    sys.exit(aplicacion.exec_())
