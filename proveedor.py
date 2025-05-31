# Tienda Pitico - Proveedor
# MARISA RIOS DE PAZ S4A

import wx
from db import conexion, cursor


class ProveedorFrame(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title='Proveedor', size=(500, 500))
        self.panel = wx.Panel(self)

        self.crear_interfaz()
        self.Centre()

    def crear_interfaz(self):
        # Título
        titulo = wx.StaticText(self.panel, label="Proveedor", pos=(180, 30))
        fuente_titulo = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        titulo.SetFont(fuente_titulo)

        # Botón Regresar
        self.boton_regresar = wx.Button(self.panel, label="Regresar", pos=(20, 20), size=(80, 30))
        self.boton_regresar.SetBackgroundColour(wx.Colour(178, 34, 34))  # Rojo oscuro
        self.boton_regresar.SetForegroundColour(wx.WHITE)
        self.boton_regresar.Bind(wx.EVT_BUTTON, self.volver_menu)

        # Campos del formulario
        wx.StaticText(self.panel, label="Id Proveedor:", pos=(50, 100))
        self.id_proveedor_entry = wx.TextCtrl(self.panel, pos=(180, 100), size=(200, -1))
        self.id_proveedor_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Nombre:", pos=(50, 140))
        self.nombre_entry = wx.TextCtrl(self.panel, pos=(180, 140), size=(200, -1))
        self.nombre_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Contacto:", pos=(50, 180))
        self.contacto_entry = wx.TextCtrl(self.panel, pos=(180, 180), size=(200, -1))
        self.contacto_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Telefono:", pos=(50, 220))
        self.telefono_entry = wx.TextCtrl(self.panel, pos=(180, 220), size=(200, -1))
        self.telefono_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Email:", pos=(50, 260))
        self.email_entry = wx.TextCtrl(self.panel, pos=(180, 260), size=(200, -1))
        self.email_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Dirección:", pos=(50, 300))
        self.direccion_entry = wx.TextCtrl(self.panel, pos=(180, 300), size=(200, -1))
        self.direccion_entry.SetBackgroundColour("light gray")

        # Botones
        boton_ancho = 100
        espaciado = 10
        total_botones = 4 * boton_ancho + 3 * espaciado
        inicio_x = (500 - total_botones) // 2
        y_botones = 355

        self.boton_crear = wx.Button(self.panel, label="Crear", pos=(inicio_x, y_botones), size=(boton_ancho, 30))
        self.boton_buscar = wx.Button(self.panel, label="Buscar", pos=(inicio_x + (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
        self.boton_actualizar = wx.Button(self.panel, label="Actualizar", pos=(inicio_x + 2 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
        self.boton_eliminar = wx.Button(self.panel, label="Eliminar", pos=(inicio_x + 3 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))

        # Asignar eventos
        self.boton_crear.Bind(wx.EVT_BUTTON, self.crear_proveedor)
        self.boton_buscar.Bind(wx.EVT_BUTTON, self.buscar_proveedor)
        self.boton_actualizar.Bind(wx.EVT_BUTTON, self.actualizar_proveedor)
        self.boton_eliminar.Bind(wx.EVT_BUTTON, self.eliminar_proveedor)

    def volver_menu(self, event):
        from menu import MenuPrincipal
        frame = MenuPrincipal()
        frame.Show()
        self.Close()

    def crear_proveedor(self, event):
        id_proveedor = self.id_proveedor_entry.GetValue()
        nombre = self.nombre_entry.GetValue()
        contacto = self.contacto_entry.GetValue()
        telefono = self.telefono_entry.GetValue()
        email = self.email_entry.GetValue()
        direccion = self.direccion_entry.GetValue()

        try:
            sql = "INSERT INTO proveedor (id_proveedor, nombre, contacto, telefono, email, direccion) VALUES (%s, %s, %s, %s, %s, %s)"
            valores = (id_proveedor, nombre, contacto, telefono, email, direccion)
            cursor.execute(sql, valores)
            conexion.commit()
            wx.MessageBox("Proveedor creado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error al crear proveedor:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def buscar_proveedor(self, event):
        id_proveedor = self.id_proveedor_entry.GetValue()

        try:
            sql = "SELECT nombre, contacto, telefono, email, direccion FROM proveedor WHERE id_proveedor = %s"
            cursor.execute(sql, (id_proveedor,))
            resultado = cursor.fetchone()
            if resultado:
                self.nombre_entry.SetValue(resultado[0])
                self.contacto_entry.SetValue(resultado[1])
                self.telefono_entry.SetValue(resultado[2])
                self.email_entry.SetValue(resultado[3])
                self.direccion_entry.SetValue(resultado[4])
            else:
                wx.MessageBox("Proveedor no encontrado", "Aviso", wx.OK | wx.ICON_WARNING)
        except Exception as e:
            wx.MessageBox(f"Error al buscar proveedor:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def actualizar_proveedor(self, event):
        id_proveedor = self.id_proveedor_entry.GetValue()
        nombre = self.nombre_entry.GetValue()
        contacto = self.contacto_entry.GetValue()
        telefono = self.telefono_entry.GetValue()
        email = self.email_entry.GetValue()
        direccion = self.direccion_entry.GetValue()

        try:
            sql = "UPDATE proveedor SET nombre=%s, contacto=%s, telefono=%s, email=%s, direccion=%s WHERE id_proveedor=%s"
            valores = (nombre, contacto, telefono, email, direccion, id_proveedor)
            cursor.execute(sql, valores)
            conexion.commit()
            wx.MessageBox("Proveedor actualizado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error al actualizar proveedor:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def eliminar_proveedor(self, event):
        id_proveedor = self.id_proveedor_entry.GetValue()

        try:
            sql = "DELETE FROM proveedor WHERE id_proveedor = %s"
            cursor.execute(sql, (id_proveedor,))
            conexion.commit()
            wx.MessageBox("Proveedor eliminado", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error al eliminar proveedor:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)