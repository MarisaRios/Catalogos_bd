# Tienda Pitico - Inventario
# MARISA RIOS DE PAZ S4A

import wx
from datetime import datetime
from db import conexion, cursor


class InventarioFrame(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title='Inventario', size=(600, 400))
        self.panel = wx.Panel(self)

        self.crear_interfaz()
        self.Centre()

    def crear_interfaz(self):
        # Título
        titulo = wx.StaticText(self.panel, label="Inventario", pos=(180, 30))
        fuente_titulo = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        titulo.SetFont(fuente_titulo)

        # Campos del formulario
        wx.StaticText(self.panel, label="Codigo de barras:", pos=(50, 100))
        self.codigo_barras_entry = wx.TextCtrl(self.panel, pos=(180, 100), size=(200, -1))
        self.codigo_barras_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Cantidad:", pos=(50, 140))
        self.cantidad_entry = wx.TextCtrl(self.panel, pos=(180, 140), size=(200, -1))
        self.cantidad_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Fecha de actualización:", pos=(50, 180))
        self.fecha_actualizacion_entry = wx.TextCtrl(self.panel, pos=(180, 180), size=(200, -1))
        self.fecha_actualizacion_entry.SetHint("yyyy/mm/dd hh:mm:ss")
        self.fecha_actualizacion_entry.SetBackgroundColour("light gray")

        self.boton_fecha_actual = wx.Button(self.panel, label="Fecha actual", pos=(390, 180), size=(100, 25))

        # Botones
        boton_ancho = 100
        espaciado = 10
        total_botones = 4 * boton_ancho + 3 * espaciado
        inicio_x = (500 - total_botones) // 2
        y_botones = 240

        self.boton_crear = wx.Button(self.panel, label="Crear", pos=(inicio_x, y_botones), size=(boton_ancho, 30))
        self.boton_buscar = wx.Button(self.panel, label="Buscar", pos=(inicio_x + (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
        self.boton_actualizar = wx.Button(self.panel, label="Actualizar", pos=(inicio_x + 2 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
        self.boton_eliminar = wx.Button(self.panel, label="Eliminar", pos=(inicio_x + 3 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))

        # Asignar eventos
        self.boton_crear.Bind(wx.EVT_BUTTON, self.crear_inventario)
        self.boton_buscar.Bind(wx.EVT_BUTTON, self.buscar_inventario)
        self.boton_actualizar.Bind(wx.EVT_BUTTON, self.actualizar_inventario)
        self.boton_eliminar.Bind(wx.EVT_BUTTON, self.eliminar_inventario)
        self.boton_fecha_actual.Bind(wx.EVT_BUTTON, self.insertar_fecha_actual)

    def crear_inventario(self, event):
        codigo = self.codigo_barras_entry.GetValue()
        cantidad = self.cantidad_entry.GetValue()
        fecha = self.fecha_actualizacion_entry.GetValue()

        if not fecha.strip():
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            sql = "INSERT INTO inventario (codigo_barras, cantidad, fecha_actualizacion) VALUES (%s, %s, %s)"
            valores = (codigo, cantidad, fecha)
            cursor.execute(sql, valores)
            conexion.commit()
            wx.MessageBox("Inventario creado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error al crear inventario:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def buscar_inventario(self, event):
        codigo = self.codigo_barras_entry.GetValue()

        try:
            sql = "SELECT cantidad, fecha_actualizacion FROM inventario WHERE codigo_barras = %s"
            cursor.execute(sql, (codigo,))
            resultado = cursor.fetchone()
            if resultado:
                self.cantidad_entry.SetValue(str(resultado[0]))
                self.fecha_actualizacion_entry.SetValue(str(resultado[1]))
            else:
                wx.MessageBox("Inventario no encontrado", "Aviso", wx.OK | wx.ICON_WARNING)
        except Exception as e:
            wx.MessageBox(f"Error al buscar inventario:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def actualizar_inventario(self, event):
        codigo = self.codigo_barras_entry.GetValue()
        cantidad = self.cantidad_entry.GetValue()
        fecha = self.fecha_actualizacion_entry.GetValue()

        if not fecha.strip():
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        try:
            sql = "UPDATE inventario SET cantidad = %s, fecha_actualizacion = %s WHERE codigo_barras = %s"
            valores = (cantidad, fecha, codigo)
            cursor.execute(sql, valores)
            conexion.commit()
            wx.MessageBox("Inventario actualizado", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error al actualizar inventario:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def eliminar_inventario(self, event):
        codigo = self.codigo_barras_entry.GetValue()

        try:
            sql = "DELETE FROM inventario WHERE codigo_barras = %s"
            cursor.execute(sql, (codigo,))
            conexion.commit()
            wx.MessageBox("Inventario eliminado", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error al eliminar inventario:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def insertar_fecha_actual(self, event):
        ahora = datetime.now()
        fecha_formateada = ahora.strftime("%Y-%m-%d %H:%M:%S")
        self.fecha_actualizacion_entry.SetValue(fecha_formateada)