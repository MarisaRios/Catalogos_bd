# Tienda Pitico - Artículos
# MARISA RIOS DE PAZ S4A

import wx
from db import conexion, cursor


class ArticuloFrame(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title='Artículos', size=(600, 500))
        self.panel = wx.Panel(self)

        self.crear_interfaz()
        self.Centre()

    def crear_interfaz(self):
        # Título
        titulo = wx.StaticText(self.panel, label="Artículos", pos=(240, 30))
        fuente_titulo = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        titulo.SetFont(fuente_titulo)

        # Campos del formulario
        wx.StaticText(self.panel, label="Código de Barras:", pos=(50, 80))
        self.codigo_barras_entry = wx.TextCtrl(self.panel, pos=(200, 80), size=(300, -1))
        self.codigo_barras_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Nombre:", pos=(50, 120))
        self.nombre_entry = wx.TextCtrl(self.panel, pos=(200, 120), size=(300, -1))
        self.nombre_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Precio:", pos=(50, 160))
        self.precio_entry = wx.TextCtrl(self.panel, pos=(200, 160), size=(100, -1))
        self.precio_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Existencia:", pos=(50, 200))
        self.existencia_entry = wx.TextCtrl(self.panel, pos=(200, 200), size=(100, -1))
        self.existencia_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Unidad:", pos=(50, 240))
        self.unidad_entry = wx.TextCtrl(self.panel, pos=(200, 240), size=(150, -1))
        self.unidad_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Descripción:", pos=(50, 280))
        self.descripcion_entry = wx.TextCtrl(self.panel, pos=(200, 280), size=(300, -1))
        self.descripcion_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="ID Categoría:", pos=(50, 320))
        self.id_categoria_entry = wx.TextCtrl(self.panel, pos=(200, 320), size=(100, -1))
        self.id_categoria_entry.SetBackgroundColour("light gray")

        # Botones
        boton_ancho = 100
        espaciado = 10
        total_botones = 4 * boton_ancho + 3 * espaciado
        inicio_x = (600 - total_botones) // 2
        y_botones = 380

        self.boton_crear = wx.Button(self.panel, label="Crear", pos=(inicio_x, y_botones), size=(boton_ancho, 30))
        self.boton_buscar = wx.Button(self.panel, label="Buscar", pos=(inicio_x + (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
        self.boton_actualizar = wx.Button(self.panel, label="Actualizar", pos=(inicio_x + 2 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
        self.boton_eliminar = wx.Button(self.panel, label="Eliminar", pos=(inicio_x + 3 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))

        self.boton_regresar = wx.Button(self.panel, label="Regresar", pos=(20, 20), size=(80, 30))
        self.boton_regresar.SetBackgroundColour(wx.Colour(178, 34, 34))  # Rojo oscuro
        self.boton_regresar.SetForegroundColour(wx.WHITE)
        self.boton_regresar.Bind(wx.EVT_BUTTON, self.volver_menu)

        # Asignar eventos
        self.boton_crear.Bind(wx.EVT_BUTTON, self.crear_articulo)
        self.boton_buscar.Bind(wx.EVT_BUTTON, self.buscar_articulo)
        self.boton_actualizar.Bind(wx.EVT_BUTTON, self.actualizar_articulo)
        self.boton_eliminar.Bind(wx.EVT_BUTTON, self.eliminar_articulo)

    def volver_menu(self, event):
        from menu import MenuPrincipal
        frame = MenuPrincipal()
        frame.Show()
        self.Close()

    def crear_articulo(self, event):
        codigo_barras = self.codigo_barras_entry.GetValue()
        nombre = self.nombre_entry.GetValue()
        precio = self.precio_entry.GetValue()
        existencia = self.existencia_entry.GetValue()
        unidad = self.unidad_entry.GetValue()
        descripcion = self.descripcion_entry.GetValue()
        id_categoria = self.id_categoria_entry.GetValue()

        try:
            sql = """INSERT INTO articulos (codigo_barras, nombre, precio, existencia, unidad, descripcion, id_categoria) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            valores = (codigo_barras, nombre, float(precio), int(existencia), unidad, descripcion, int(id_categoria))
            cursor.execute(sql, valores)
            conexion.commit()
            wx.MessageBox("Artículo creado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error al crear artículo:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def buscar_articulo(self, event):
        codigo_barras = self.codigo_barras_entry.GetValue()

        try:
            sql = "SELECT nombre, precio, existencia, unidad, descripcion, id_categoria FROM articulos WHERE codigo_barras = %s"
            cursor.execute(sql, (codigo_barras,))
            resultado = cursor.fetchone()
            if resultado:
                self.nombre_entry.SetValue(resultado[0])
                self.precio_entry.SetValue(str(resultado[1]))
                self.existencia_entry.SetValue(str(resultado[2]))
                self.unidad_entry.SetValue(resultado[3] or "")
                self.descripcion_entry.SetValue(resultado[4] or "")
                self.id_categoria_entry.SetValue(str(resultado[5]))
            else:
                wx.MessageBox("Artículo no encontrado", "Aviso", wx.OK | wx.ICON_WARNING)
        except Exception as e:
            wx.MessageBox(f"Error al buscar artículo:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def actualizar_articulo(self, event):
        codigo_barras = self.codigo_barras_entry.GetValue()
        nombre = self.nombre_entry.GetValue()
        precio = self.precio_entry.GetValue()
        existencia = self.existencia_entry.GetValue()
        unidad = self.unidad_entry.GetValue()
        descripcion = self.descripcion_entry.GetValue()
        id_categoria = self.id_categoria_entry.GetValue()

        try:
            sql = """UPDATE articulos SET nombre = %s, precio = %s, existencia = %s, unidad = %s, descripcion = %s, 
                     id_categoria = %s WHERE codigo_barras = %s"""
            valores = (nombre, float(precio), int(existencia), unidad, descripcion, int(id_categoria), codigo_barras)
            cursor.execute(sql, valores)
            conexion.commit()
            wx.MessageBox("Artículo actualizado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error al actualizar artículo:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def eliminar_articulo(self, event):
        codigo_barras = self.codigo_barras_entry.GetValue()

        try:
            sql = "DELETE FROM articulos WHERE codigo_barras = %s"
            cursor.execute(sql, (codigo_barras,))
            conexion.commit()
            wx.MessageBox("Artículo eliminado", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error al eliminar artículo:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)