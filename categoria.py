# Tienda Pitico - Categorías
# MARISA RIOS DE PAZ S4A

import wx
from db import conexion, cursor


class CategoriaFrame(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title='Categorías', size=(500, 400))
        self.panel = wx.Panel(self)

        self.crear_interfaz()
        self.Centre()

    def crear_interfaz(self):
        # Título
        titulo = wx.StaticText(self.panel, label="Categorías", pos=(180, 30))
        fuente_titulo = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        titulo.SetFont(fuente_titulo)

        # Campos del formulario
        wx.StaticText(self.panel, label="Id Categoría:", pos=(50, 100))
        self.id_categoria_entry = wx.TextCtrl(self.panel, pos=(180, 100), size=(200, -1))
        self.id_categoria_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Nombre:", pos=(50, 140))
        self.nombre_entry = wx.TextCtrl(self.panel, pos=(180, 140), size=(200, -1))
        self.nombre_entry.SetBackgroundColour("light gray")

        # Botones
        boton_ancho = 100
        espaciado = 10
        total_botones = 4 * boton_ancho + 3 * espaciado
        inicio_x = (500 - total_botones) // 2
        y_botones = 220

        self.boton_crear = wx.Button(self.panel, label="Crear", pos=(inicio_x, y_botones), size=(boton_ancho, 30))
        self.boton_buscar = wx.Button(self.panel, label="Buscar", pos=(inicio_x + (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
        self.boton_actualizar = wx.Button(self.panel, label="Actualizar", pos=(inicio_x + 2 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
        self.boton_eliminar = wx.Button(self.panel, label="Eliminar", pos=(inicio_x + 3 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))

        self.boton_regresar = wx.Button(self.panel, label="Regresar", pos=(20, 20), size=(80, 30))
        self.boton_regresar.SetBackgroundColour(wx.Colour(178, 34, 34))
        self.boton_regresar.SetForegroundColour(wx.WHITE)
        self.boton_regresar.Bind(wx.EVT_BUTTON, self.volver_menu)

        # Asignar eventos
        self.boton_crear.Bind(wx.EVT_BUTTON, self.crear_categoria)
        self.boton_buscar.Bind(wx.EVT_BUTTON, self.buscar_categoria)
        self.boton_actualizar.Bind(wx.EVT_BUTTON, self.actualizar_categoria)
        self.boton_eliminar.Bind(wx.EVT_BUTTON, self.eliminar_categoria)

    def volver_menu(self, event):
        from menu import MenuPrincipal
        frame = MenuPrincipal()
        frame.Show()
        self.Close()

    def crear_categoria(self, event):
        id_categoria = self.id_categoria_entry.GetValue()
        nombre = self.nombre_entry.GetValue()

        try:
            sql = "INSERT INTO categoria (id_categoria, nombre) VALUES (%s, %s)"
            valores = (id_categoria, nombre)
            cursor.execute(sql, valores)
            conexion.commit()
            wx.MessageBox("Categoría creada exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error al crear categoría:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def buscar_categoria(self, event):
        id_categoria = self.id_categoria_entry.GetValue()

        try:
            sql = "SELECT nombre FROM categoria WHERE id_categoria = %s"
            cursor.execute(sql, (id_categoria,))
            resultado = cursor.fetchone()
            if resultado:
                self.nombre_entry.SetValue(resultado[0])
            else:
                wx.MessageBox("Categoría no encontrada", "Aviso", wx.OK | wx.ICON_WARNING)
        except Exception as e:
            wx.MessageBox(f"Error al buscar categoría:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def actualizar_categoria(self, event):
        id_categoria = self.id_categoria_entry.GetValue()
        nombre = self.nombre_entry.GetValue()

        try:
            sql = "UPDATE categoria SET nombre = %s WHERE id_categoria = %s"
            valores = (nombre, id_categoria)
            cursor.execute(sql, valores)
            conexion.commit()
            wx.MessageBox("Categoría actualizada correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error al actualizar categoría:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def eliminar_categoria(self, event):
        id_categoria = self.id_categoria_entry.GetValue()

        try:
            sql = "DELETE FROM categoria WHERE id_categoria = %s"
            cursor.execute(sql, (id_categoria,))
            conexion.commit()
            wx.MessageBox("Categoría eliminada", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error al eliminar categoría:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)