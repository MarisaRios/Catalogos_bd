import wx
from db import conexion, cursor


class ClienteFrame(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title='Clientes', size=(900, 450))
        self.panel = wx.Panel(self)

        self.crear_interfaz()
        self.Centre()

    def crear_interfaz(self):
        # Título
        titulo = wx.StaticText(self.panel, label="Clientes", pos=(380, 30))
        fuente_titulo = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        titulo.SetFont(fuente_titulo)

        # Campos del formulario
        wx.StaticText(self.panel, label="Teléfono:", pos=(50, 80))
        self.telefono_entry = wx.TextCtrl(self.panel, pos=(180, 80), size=(200, -1))
        self.telefono_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Nombre:", pos=(50, 120))
        self.nombre_entry = wx.TextCtrl(self.panel, pos=(180, 120), size=(200, -1))
        self.nombre_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Apellido:", pos=(50, 160))
        self.apellido_entry = wx.TextCtrl(self.panel, pos=(180, 160), size=(200, -1))
        self.apellido_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Email:", pos=(50, 200))
        self.email_entry = wx.TextCtrl(self.panel, pos=(180, 200), size=(200, -1))
        self.email_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Dirección:", pos=(50, 240))
        self.direccion_entry = wx.TextCtrl(self.panel, pos=(180, 240), size=(200, -1))
        self.direccion_entry.SetBackgroundColour("light gray")

        # Botones
        boton_ancho = 100
        espaciado = 10
        total_botones = 4 * boton_ancho + 3 * espaciado
        inicio_x = 10
        y_botones = 290

        self.boton_crear = wx.Button(self.panel, label="Crear", pos=(inicio_x, y_botones), size=(boton_ancho, 30))
        self.boton_buscar = wx.Button(self.panel, label="Buscar", pos=(inicio_x + (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
        self.boton_actualizar = wx.Button(self.panel, label="Actualizar", pos=(inicio_x + 2 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
        self.boton_eliminar = wx.Button(self.panel, label="Eliminar", pos=(inicio_x + 3 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))

        self.boton_regresar = wx.Button(self.panel, label="Regresar", pos=(20, 20), size=(80, 30))
        self.boton_regresar.SetBackgroundColour(wx.Colour(178, 34, 34))  # Rojo oscuro
        self.boton_regresar.SetForegroundColour(wx.WHITE)
        self.boton_regresar.Bind(wx.EVT_BUTTON, self.volver_menu)

        # Lista de clientes
        self.lista_clientes = wx.ListCtrl(
            self.panel,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN,
            pos=(450, 80),
            size=(400, 300)
        )
        self.lista_clientes.InsertColumn(0, "Teléfono", width=100)
        self.lista_clientes.InsertColumn(1, "Nombre", width=100)
        self.lista_clientes.InsertColumn(2, "Apellido", width=100)
        self.lista_clientes.InsertColumn(3, "Email", width=100)
        self.lista_clientes.InsertColumn(4, "Dirección", width=150)

        # Eventos
        self.lista_clientes.Bind(wx.EVT_LIST_ITEM_SELECTED, self.seleccionar_cliente)
        self.boton_buscar.Bind(wx.EVT_BUTTON, self.buscar_cliente)
        self.boton_crear.Bind(wx.EVT_BUTTON, self.crear_cliente)
        self.boton_actualizar.Bind(wx.EVT_BUTTON, self.actualizar_cliente)
        self.boton_eliminar.Bind(wx.EVT_BUTTON, self.eliminar_cliente)

        self.cargar_lista_clientes()

    def seleccionar_cliente(self, event):
        """Llena los campos cuando se hace doble clic en un elemento de la lista"""
        index = event.GetIndex()
        telefono = self.lista_clientes.GetItemText(index, col=0)
        nombre = self.lista_clientes.GetItemText(index, col=1)
        apellido = self.lista_clientes.GetItemText(index, col=2)
        email = self.lista_clientes.GetItemText(index, col=3)
        direccion = self.lista_clientes.GetItemText(index, col=4)

        self.telefono_entry.SetValue(telefono)
        self.nombre_entry.SetValue(nombre)
        self.apellido_entry.SetValue(apellido)
        self.email_entry.SetValue(email)
        self.direccion_entry.SetValue(direccion)

    def volver_menu(self, event):
        from menu import MenuPrincipal
        frame = MenuPrincipal()
        frame.Show()
        self.Close()

    def cargar_lista_clientes(self):
        self.lista_clientes.DeleteAllItems()

        try:
            sql = "SELECT telefono, nombre, apellido, email, direccion FROM clientes"
            cursor.execute(sql)
            resultados = cursor.fetchall()

            for idx, row in enumerate(resultados):
                # Asegurarse de que los valores no sean None
                telefono = str(row[0]) if row[0] is not None else ""
                nombre = row[1] if row[1] is not None else ""
                apellido = row[2] if row[2] is not None else ""
                email = row[3] if row[3] is not None else ""
                direccion = row[4] if row[4] is not None else ""

                # Insertar fila en la lista
                self.lista_clientes.InsertItem(idx, telefono)  # Teléfono
                self.lista_clientes.SetItem(idx, 1, nombre)     # Nombre
                self.lista_clientes.SetItem(idx, 2, apellido)   # Apellido
                self.lista_clientes.SetItem(idx, 3, email)      # Email
                self.lista_clientes.SetItem(idx, 4, direccion)  # Dirección

        except Exception as e:
            wx.MessageBox(f"Error al cargar lista de clientes:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def limpiar_campos(self):
        self.telefono_entry.Clear()
        self.nombre_entry.Clear()
        self.apellido_entry.Clear()
        self.email_entry.Clear()
        self.direccion_entry.Clear()

    def crear_cliente(self, event):
        telefono = self.telefono_entry.GetValue().strip()
        nombre = self.nombre_entry.GetValue().strip()
        apellido = self.apellido_entry.GetValue().strip()
        email = self.email_entry.GetValue().strip()
        direccion = self.direccion_entry.GetValue().strip()

        if not telefono or not nombre or not apellido:
            wx.MessageBox("Por favor complete los campos obligatorios", "Advertencia", wx.OK | wx.ICON_WARNING)
            return

        try:
            sql = "INSERT INTO clientes (telefono, nombre, apellido, email, direccion) VALUES (%s, %s, %s, %s, %s)"
            valores = (telefono, nombre, apellido, email, direccion)
            cursor.execute(sql, valores)
            conexion.commit()
            wx.MessageBox("Cliente creado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.limpiar_campos()
            self.cargar_lista_clientes()
        except Exception as e:
            wx.MessageBox(f"Error al crear cliente:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def buscar_cliente(self, event):
        telefono = self.telefono_entry.GetValue().strip()
        email = self.email_entry.GetValue().strip()

        condiciones = []
        valores = []

        if telefono:
            condiciones.append("telefono = %s")
            valores.append(telefono)
        if email:
            condiciones.append("email = %s")
            valores.append(email)

        if not condiciones:
            wx.MessageBox("Escriba un teléfono o correo electrónico para buscar", "Aviso", wx.OK | wx.ICON_INFORMATION)
            return

        sql = "SELECT telefono, nombre, apellido, email, direccion FROM clientes WHERE " + " OR ".join(condiciones)

        try:
            cursor.execute(sql, tuple(valores))
            resultado = cursor.fetchone()

            if resultado:
                self.telefono_entry.SetValue(str(resultado[0]))
                self.nombre_entry.SetValue(resultado[1])
                self.apellido_entry.SetValue(resultado[2])
                self.email_entry.SetValue(resultado[3])
                self.direccion_entry.SetValue(resultado[4])
            else:
                wx.MessageBox("Cliente no encontrado", "Aviso", wx.OK | wx.ICON_WARNING)
        except Exception as e:
            wx.MessageBox(f"Error al buscar cliente:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def actualizar_cliente(self, event):
        telefono = self.telefono_entry.GetValue().strip()
        nombre = self.nombre_entry.GetValue().strip()
        apellido = self.apellido_entry.GetValue().strip()
        email = self.email_entry.GetValue().strip()
        direccion = self.direccion_entry.GetValue().strip()

        if not telefono:
            wx.MessageBox("Debe ingresar el teléfono del cliente a actualizar", "Advertencia", wx.OK | wx.ICON_WARNING)
            return

        try:
            sql = "UPDATE clientes SET nombre = %s, apellido = %s, email = %s, direccion = %s WHERE telefono = %s"
            valores = (nombre, apellido, email, direccion, telefono)
            cursor.execute(sql, valores)
            conexion.commit()
            wx.MessageBox("Cliente actualizado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.limpiar_campos()
            self.cargar_lista_clientes()
        except Exception as e:
            wx.MessageBox(f"Error al actualizar cliente:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def eliminar_cliente(self, event):
        telefono = self.telefono_entry.GetValue().strip()

        if not telefono:
            wx.MessageBox("Debe ingresar el teléfono del cliente a eliminar", "Advertencia", wx.OK | wx.ICON_WARNING)
            return

        try:
            sql = "DELETE FROM clientes WHERE telefono = %s"
            cursor.execute(sql, (telefono,))
            conexion.commit()
            wx.MessageBox("Cliente eliminado", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.limpiar_campos()
            self.cargar_lista_clientes()
        except Exception as e:
            wx.MessageBox(f"Error al eliminar cliente:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)