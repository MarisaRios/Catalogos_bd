# Tienda Pitico - Clientes
# MARISA RIOS DE PAZ S4A

import wx
from db import conexion, cursor


class ClienteFrame(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title='Clientes', size=(500, 400))
        self.panel = wx.Panel(self)

        self.crear_interfaz()
        self.Centre()

    def crear_interfaz(self):
        # Título
        titulo = wx.StaticText(self.panel, label="Clientes", pos=(180, 30))
        fuente_titulo = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        titulo.SetFont(fuente_titulo)

        # Campos del formulario
        wx.StaticText(self.panel, label="Telefono:", pos=(50, 100))
        self.telefono_entry = wx.TextCtrl(self.panel, pos=(180, 100), size=(200, -1))
        self.telefono_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Nombre:", pos=(50, 140))
        self.nombre_entry = wx.TextCtrl(self.panel, pos=(180, 140), size=(200, -1))
        self.nombre_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Apellido:", pos=(50, 180))
        self.apellido_entry = wx.TextCtrl(self.panel, pos=(180, 180), size=(200, -1))
        self.apellido_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Email:", pos=(50, 220))
        self.email_entry = wx.TextCtrl(self.panel, pos=(180, 220), size=(200, -1))
        self.email_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Dirección:", pos=(50, 260))
        self.direccion_entry = wx.TextCtrl(self.panel, pos=(180, 260), size=(200, -1))
        self.direccion_entry.SetBackgroundColour("light gray")

        # Botones
        boton_ancho = 100
        espaciado = 10
        total_botones = 4 * boton_ancho + 3 * espaciado
        inicio_x = (500 - total_botones) // 2
        y_botones = 290

        self.boton_crear = wx.Button(self.panel, label="Crear", pos=(inicio_x, y_botones), size=(boton_ancho, 30))
        self.boton_buscar = wx.Button(self.panel, label="Buscar", pos=(inicio_x + (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
        self.boton_actualizar = wx.Button(self.panel, label="Actualizar", pos=(inicio_x + 2 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
        self.boton_eliminar = wx.Button(self.panel, label="Eliminar", pos=(inicio_x + 3 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))

        self.boton_regresar = wx.Button(self.panel, label="Regresar", pos=(20, 20), size=(80, 30))
        self.boton_regresar.SetBackgroundColour(wx.Colour(178, 34, 34))  # Rojo oscuro
        self.boton_regresar.SetForegroundColour(wx.WHITE)
        self.boton_regresar.Bind(wx.EVT_BUTTON, self.volver_menu)

        # Conectar botones con funciones
        self.boton_crear.Bind(wx.EVT_BUTTON, self.crear_cliente)
        self.boton_buscar.Bind(wx.EVT_BUTTON, self.buscar_cliente)
        self.boton_actualizar.Bind(wx.EVT_BUTTON, self.actualizar_cliente)
        self.boton_eliminar.Bind(wx.EVT_BUTTON, self.eliminar_cliente)

    def volver_menu(self, event):
        from menu import MenuPrincipal
        frame = MenuPrincipal()
        frame.Show()
        self.Close()

    def crear_cliente(self, event):
        telefono = self.telefono_entry.GetValue()
        nombre = self.nombre_entry.GetValue()
        apellido = self.apellido_entry.GetValue()
        email = self.email_entry.GetValue()
        direccion = self.direccion_entry.GetValue()

        try:
            sql = "INSERT INTO clientes (telefono, nombre, apellido, email, direccion) VALUES (%s, %s, %s, %s, %s)"
            valores = (telefono, nombre, apellido, email, direccion)
            cursor.execute(sql, valores)
            conexion.commit()
            wx.MessageBox("Cliente creado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error al crear cliente:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def buscar_cliente(self, event):
        telefono = self.telefono_entry.GetValue()

        try:
            sql = "SELECT nombre, apellido, email, direccion FROM clientes WHERE telefono = %s"
            cursor.execute(sql, (telefono,))
            resultado = cursor.fetchone()
            if resultado:
                self.nombre_entry.SetValue(resultado[0])
                self.apellido_entry.SetValue(resultado[1])
                self.email_entry.SetValue(resultado[2])
                self.direccion_entry.SetValue(resultado[3])
            else:
                wx.MessageBox("Cliente no encontrado", "Aviso", wx.OK | wx.ICON_WARNING)
        except Exception as e:
            wx.MessageBox(f"Error al buscar cliente:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def actualizar_cliente(self, event):
        telefono = self.telefono_entry.GetValue()
        nombre = self.nombre_entry.GetValue()
        apellido = self.apellido_entry.GetValue()
        email = self.email_entry.GetValue()
        direccion = self.direccion_entry.GetValue()

        try:
            sql = "UPDATE clientes SET nombre = %s, apellido = %s, email = %s, direccion = %s WHERE telefono = %s"
            valores = (nombre, apellido, email, direccion, telefono)
            cursor.execute(sql, valores)
            conexion.commit()
            wx.MessageBox("Cliente actualizado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error al actualizar cliente:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def eliminar_cliente(self, event):
        telefono = self.telefono_entry.GetValue()

        try:
            sql = "DELETE FROM clientes WHERE telefono = %s"
            cursor.execute(sql, (telefono,))
            conexion.commit()
            wx.MessageBox("Cliente eliminado", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error al eliminar cliente:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)