import sys
from PyQt5 import QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QLabel, QDesktopWidget,
    QLineEdit, QPushButton, QCheckBox, QTimeEdit, QFileDialog, QTextEdit,
    QVBoxLayout, QWidget, QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import QTime


class TareasEmpleada(QMainWindow):
    def __init__(self):
        super(TareasEmpleada, self).__init__()

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
        fuente = QFont("Andale Mono", 14)

        # Layout principal
        layout_principal = QVBoxLayout()

        # Widget contenedor para tareas
        widget_tareas = QWidget(self)
        widget_tareas_layout = QVBoxLayout(widget_tareas)

        # Campos para mostrar hasta 5 tareas
        self.campos_tareas = []

        for i in range(5):
            tarea_layout = QHBoxLayout()

            etiqueta_tarea = QLabel(f"Tarea {i + 1}", self)
            etiqueta_tarea.setFont(fuente)

            editar_tarea = QLineEdit(self)
            editar_tarea.setReadOnly(True)
            editar_tarea.setFixedSize(180, 40)

            etiqueta_observaciones = QLabel(f"Observaciones {i + 1}", self)
            etiqueta_observaciones.setFont(fuente)
            etiqueta_observaciones.setFixedWidth(200)

            editar_observaciones = QTextEdit(self)
            editar_observaciones.setReadOnly(True)
            editar_observaciones.setFixedSize(200, 100)

            etiqueta_hora = QLabel(f"Hora de la Tarea {i + 1}", self)
            etiqueta_hora.setFont(fuente)
            etiqueta_hora.setFixedWidth(200)

            editar_hora_tarea = QTimeEdit(self)
            editar_hora_tarea.setReadOnly(True)
            editar_hora_tarea.setFixedSize(120, 30)

            checkbox_completado = QCheckBox(f"Tarea {i + 1} Completada", self)

            boton_subir_imagen = QPushButton(f"Subir Imagen {i + 1}", self)
            boton_subir_imagen.clicked.connect(lambda _, index=i: self.subir_imagen(index))

            # Nuevo botón "Enviar" para cada tarea
            boton_enviar = QPushButton(f"Enviar {i + 1}", self)
            boton_enviar.clicked.connect(lambda _, index=i: self.enviar_tarea(index))

            tarea_layout.addWidget(etiqueta_tarea)
            tarea_layout.addWidget(editar_tarea)
            tarea_layout.addWidget(etiqueta_observaciones)
            tarea_layout.addWidget(editar_observaciones)
            tarea_layout.addWidget(etiqueta_hora)
            tarea_layout.addWidget(editar_hora_tarea)
            tarea_layout.addWidget(checkbox_completado)
            tarea_layout.addWidget(boton_subir_imagen)
            tarea_layout.addWidget(boton_enviar)

            widget_tareas_layout.addLayout(tarea_layout)

            self.campos_tareas.append({
                'Editar Tarea': editar_tarea,
                'Editar Observaciones': editar_observaciones,
                'Editar Hora Tarea': editar_hora_tarea,
                'Checkbox Completado': checkbox_completado,
                'Boton Subir Imagen': boton_subir_imagen,
                'Boton Enviar': boton_enviar,
                'Ruta Imagen': ''  # Agregar campo para la ruta de la imagen
            })

        # Añadir el widget de tareas al layout principal
        layout_principal.addWidget(widget_tareas)

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
            # Guardar la ruta de la imagen en la lista
            self.campos_tareas[tarea_index]['Ruta Imagen'] = ruta_archivo
            print(f"Imagen para Tarea {tarea_index + 1}: {ruta_archivo}")

    def enviar_tarea(self, tarea_index):
        # Verificar si el checkbox está marcado
        if self.campos_tareas[tarea_index]['Checkbox Completado'].isChecked():
            # Obtener detalles de la tarea
            tarea = self.campos_tareas[tarea_index]['Editar Tarea'].text()
            observaciones = self.campos_tareas[tarea_index]['Editar Observaciones'].toPlainText()
            hora_tarea = self.campos_tareas[tarea_index]['Editar Hora Tarea'].time()
            ruta_imagen = self.campos_tareas[tarea_index]['Ruta Imagen']

            # Validaciones
            if not tarea or not observaciones or not hora_tarea.isValid():
                QMessageBox.critical(self, "Error", "Complete todos los campos antes de enviar la tarea.")
                return

            # Crear una cadena con los detalles de la tarea
            detalles_tarea = f"Tarea: {tarea}\nObservaciones: {observaciones}\nHora de Tarea: {hora_tarea.toString()}"

            if ruta_imagen:
                detalles_tarea += f"\nRuta de Imagen: {ruta_imagen}"

            # Agregar una línea de guiones como separador
            detalles_tarea += "\n---\n"

            # Guardar los detalles en el archivo tareas_completadas.txt
            with open("tareas_completadas.txt", "a") as archivo:
                archivo.write(detalles_tarea)

            QMessageBox.information(self, "Éxito", f"Tarea {tarea_index + 1} enviada y guardada en tareas_completadas.txt.")
            print(f"Tarea {tarea_index + 1} enviada y guardada en tareas_completadas.txt.")
        else:
            QMessageBox.warning(self, "Error", f"Marque la casilla de verificación para completar la tarea {tarea_index + 1}.")

    def mostrar_detalles_tarea(self):
        # Leer detalles de la tarea desde el archivo
        try:
            with open("detalles_tarea.txt", "r") as archivo:
                lineas = archivo.readlines()
                if lineas:
                    # Dividir las líneas en bloques de 5 para cada tarea
                    bloques_tareas = [lineas[i:i + 5] for i in range(0, len(lineas), 5)]

                    # Recorrer cada bloque de tarea
                    for i, bloque in enumerate(bloques_tareas):
                        detalles_tarea = {}
                        for linea in bloque:
                            if "Tarea:" in linea:
                                tarea = linea.split(":")[1].strip()
                                detalles_tarea['Tarea'] = tarea
                            elif "Observaciones:" in linea:
                                observaciones = linea.split(":")[1].strip()
                                detalles_tarea['Observaciones'] = observaciones
                            elif "Hora de Alarma:" in linea:
                                hora_alarma = linea.split(":")[1].strip()
                                detalles_tarea['Hora de Alarma'] = hora_alarma
                                break

                        # Mostrar detalles en la interfaz
                        self.campos_tareas[i]['Editar Tarea'].setText(detalles_tarea.get('Tarea', ''))
                        self.campos_tareas[i]['Editar Observaciones'].setPlainText(
                            detalles_tarea.get('Observaciones', ''))
                        hora_tarea = QTime.fromString(detalles_tarea.get('Hora de Alarma', ''), "HH:mm:ss")
                        self.campos_tareas[i]['Editar Hora Tarea'].setTime(hora_tarea)

        except FileNotFoundError:
            print("El archivo detalles_tarea.txt no existe.")


# Bloque principal
if __name__ == '__main__':
    aplicacion = QApplication(sys.argv)
    ventana_tareas = TareasEmpleada()
    ventana_tareas.show()
    sys.exit(aplicacion.exec_())
