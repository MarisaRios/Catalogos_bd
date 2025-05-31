# Punto de Venta - Tienda Pitico
# MARISA RIOS DE PAZ S4A

import wx
from datetime import datetime
from db import conexion, cursor


class TicketFrame(wx.Dialog):
    """Ventana que muestra el ticket formateado como una ventana modal"""
    def __init__(self, parent, titulo, contenido):
        super().__init__(parent, title=titulo, size=(400, 600))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))  # Fondo blanco

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Título del ticket
        titulo_ticket = wx.StaticText(panel, label="TIENDA PITICO")
        fuente_titulo = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        titulo_ticket.SetFont(fuente_titulo)
        titulo_ticket.SetForegroundColour(wx.BLACK)

        # Contenido del ticket
        texto_contenido = wx.TextCtrl(
            panel,
            value=contenido,
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_CENTER,
            size=(350, 500)
        )
        texto_contenido.SetBackgroundColour(wx.WHITE)
        texto_contenido.SetForegroundColour(wx.BLACK)

        # Botón Cerrar
        boton_cerrar = wx.Button(panel, label="Cerrar", size=(80, 30))
        boton_cerrar.Bind(wx.EVT_BUTTON, self.on_cerrar)

        # Layout
        sizer.Add(titulo_ticket, 0, wx.ALIGN_CENTER | wx.TOP, 20)
        sizer.Add(texto_contenido, 1, wx.EXPAND | wx.ALL, 10)
        sizer.Add(boton_cerrar, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        panel.SetSizer(sizer)

    def on_cerrar(self, event):
        self.Close()


class VentaFrame(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title="Punto de Venta", size=(950, 680))
        self.panel = wx.Panel(self)
        self.SetBackgroundColour(wx.Colour(245, 245, 245))

        # Tabla temporal para almacenar la venta
        self.temp_venta = []

        self.crear_interfaz()
        self.Centre()

    def crear_interfaz(self):
        # Título
        titulo = wx.StaticText(self.panel, label="Registrar Venta", pos=(110, 10))
        fuente_titulo = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        titulo.SetFont(fuente_titulo)

        # Botón Regresar
        self.boton_regresar = wx.Button(self.panel, label="Regresar", pos=(20, 20), size=(80, 30))
        self.boton_regresar.SetBackgroundColour(wx.Colour(178, 34, 34))  # Rojo oscuro
        self.boton_regresar.SetForegroundColour(wx.WHITE)
        self.boton_regresar.Bind(wx.EVT_BUTTON, self.volver_menu)

        # Datos del cliente y empleado
        wx.StaticText(self.panel, label="Teléfono Cliente:", pos=(30, 70))
        self.telefono_cliente = wx.TextCtrl(self.panel, pos=(180, 70), size=(200, -1))

        self.etiqueta_nombre_cliente = wx.StaticText(self.panel, label="", pos=(400, 70))
        self.etiqueta_nombre_cliente.SetForegroundColour(wx.BLUE)

        self.boton_cliente_general = wx.Button(self.panel, label="Cliente General", pos=(400, 100), size=(130, 25))
        self.boton_cliente_general.Bind(wx.EVT_BUTTON, self.usar_cliente_general)

        wx.StaticText(self.panel, label="ID Empleado:", pos=(30, 110))
        self.id_empleado = wx.TextCtrl(self.panel, pos=(180, 110), size=(200, -1))

        # Campos para artículo
        wx.StaticText(self.panel, label="Código de Barras:", pos=(30, 160))
        self.codigo_barras_entry = wx.TextCtrl(self.panel, pos=(180, 160), size=(200, -1))

        wx.StaticText(self.panel, label="Cantidad:", pos=(30, 200))
        self.cantidad_entry = wx.TextCtrl(self.panel, pos=(180, 200), size=(200, -1))

        self.boton_agregar = wx.Button(self.panel, label="Agregar Artículo", pos=(400, 180), size=(150, 30))
        self.boton_agregar.SetBackgroundColour(wx.Colour(52, 168, 83))
        self.boton_agregar.SetForegroundColour(wx.WHITE)

        self.boton_limpiar = wx.Button(self.panel, label="Limpiar", pos=(450, 500), size=(100, 40))
        self.boton_limpiar.SetBackgroundColour(wx.Colour(255, 165, 0))
        self.boton_limpiar.SetForegroundColour(wx.WHITE)
        self.boton_limpiar.Bind(wx.EVT_BUTTON, self.limpiar_formulario)

        # Lista de artículos
        self.lista_articulos = wx.ListCtrl(self.panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN,
                                          pos=(30, 250), size=(700, 200))
        self.lista_articulos.InsertColumn(0, "Código", width=100)
        self.lista_articulos.InsertColumn(1, "Nombre", width=200)
        self.lista_articulos.InsertColumn(2, "Precio Unitario", width=120)
        self.lista_articulos.InsertColumn(3, "Cantidad", width=80)
        self.lista_articulos.InsertColumn(4, "Subtotal", width=120)

        # Botón Eliminar Artículo
        self.boton_eliminar_articulo = wx.Button(self.panel, label="Eliminar Artículo", pos=(750, 300), size=(150, 30))
        self.boton_eliminar_articulo.SetBackgroundColour(wx.Colour(178, 34, 34))
        self.boton_eliminar_articulo.SetForegroundColour(wx.WHITE)
        self.boton_eliminar_articulo.Bind(wx.EVT_BUTTON, self.eliminar_articulo_seleccionado)

        # Total
        self.etiqueta_total = wx.StaticText(self.panel, label="Total: $0.00", pos=(650, 470))
        fuente_total = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.etiqueta_total.SetFont(fuente_total)

        # Botón Finalizar Venta
        self.boton_finalizar = wx.Button(self.panel, label="Finalizar Venta", pos=(650, 500), size=(180, 40))
        self.boton_finalizar.SetBackgroundColour(wx.Colour(66, 133, 244))
        self.boton_finalizar.SetForegroundColour(wx.WHITE)
        self.boton_finalizar.Bind(wx.EVT_BUTTON, self.finalizar_venta)

        # Eventos
        self.boton_agregar.Bind(wx.EVT_BUTTON, self.agregar_articulo)
        self.boton_limpiar.Bind(wx.EVT_BUTTON, self.limpiar_formulario)

    def volver_menu(self, event):
        from menu import MenuPrincipal
        frame = MenuPrincipal()
        frame.Show()
        self.Close()

    def limpiar_formulario(self, event):
        self.telefono_cliente.SetValue("")
        self.id_empleado.SetValue("")
        self.codigo_barras_entry.SetValue("")
        self.cantidad_entry.SetValue("")
        self.temp_venta.clear()
        self.lista_articulos.DeleteAllItems()
        self.etiqueta_total.SetLabel("Total: $0.00")
        self.etiqueta_nombre_cliente.SetLabel("")

    def agregar_articulo(self, event):
        codigo = self.codigo_barras_entry.GetValue().strip()
        try:
            cantidad = int(self.cantidad_entry.GetValue())
        except ValueError:
            wx.MessageBox("La cantidad debe ser un número válido.", "Error", wx.OK | wx.ICON_ERROR)
            return

        sql = "SELECT nombre, precio FROM articulos WHERE codigo_barras = %s"
        cursor.execute(sql, (codigo,))
        resultado = cursor.fetchone()

        if not resultado:
            wx.MessageBox("Artículo no encontrado.", "Error", wx.OK | wx.ICON_ERROR)
            return

        nombre, precio = resultado
        subtotal = precio * cantidad

        self.temp_venta.append({
            "codigo": codigo,
            "nombre": nombre,
            "precio": precio,
            "cantidad": cantidad,
            "subtotal": subtotal
        })

        self.actualizar_lista_articulos()
        self.codigo_barras_entry.SetValue("")
        self.cantidad_entry.SetValue("")

    def actualizar_lista_articulos(self):
        self.lista_articulos.DeleteAllItems()
        for idx, item in enumerate(self.temp_venta):
            self.lista_articulos.InsertItem(idx, item["codigo"])
            self.lista_articulos.SetItem(idx, 1, item["nombre"])
            self.lista_articulos.SetItem(idx, 2, f"${item['precio']:.2f}")
            self.lista_articulos.SetItem(idx, 3, str(item["cantidad"]))
            self.lista_articulos.SetItem(idx, 4, f"${item['subtotal']:.2f}")

        total = sum(item["subtotal"] for item in self.temp_venta)
        self.etiqueta_total.SetLabel(f"Total: ${total:.2f}")

    def eliminar_articulo_seleccionado(self, event):
        index = self.lista_articulos.GetFirstSelected()
        if index == -1:
            wx.MessageBox("Por favor, seleccione un artículo de la lista.", "Advertencia", wx.OK | wx.ICON_WARNING)
            return
        del self.temp_venta[index]
        self.actualizar_lista_articulos()

    def usar_cliente_general(self, event):
        self.telefono_cliente.SetValue("0000000000")
        self.etiqueta_nombre_cliente.SetLabel("Cliente General")
        self.nombre_cliente = "Cliente General"

    def finalizar_venta(self, event):
        telefono = self.telefono_cliente.GetValue().strip()
        id_empleado = self.id_empleado.GetValue().strip()

        if not telefono or not id_empleado:
            wx.MessageBox("Debe ingresar teléfono y ID de empleado.", "Faltan Datos", wx.OK | wx.ICON_WARNING)
            return

        try:
            id_empleado = int(id_empleado)
        except ValueError:
            wx.MessageBox("El ID del empleado debe ser un número.", "Error", wx.OK | wx.ICON_ERROR)
            return

        if not self.temp_venta:
            wx.MessageBox("No hay artículos seleccionados para vender.", "Venta vacía", wx.OK | wx.ICON_WARNING)
            return

        # Pedir forma de pago
        dlg = wx.MessageDialog(self, "Seleccione la forma de pago:", "Forma de Pago",
                            wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
        dlg.SetYesNoLabels("Tarjeta", "Efectivo")
        respuesta = dlg.ShowModal()

        if respuesta == wx.ID_CANCEL:
            return

        forma_pago = "Tarjeta" if respuesta == wx.ID_YES else "Efectivo"

        try:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            total_venta = sum(item["subtotal"] for item in self.temp_venta)

            # Validar cliente o usar cliente general
            try:
                sql_cliente = "SELECT nombre FROM clientes WHERE telefono = %s"
                cursor.execute(sql_cliente, (telefono,))
                cliente_result = cursor.fetchone()
                if cliente_result:
                    self.nombre_cliente = cliente_result[0]
                else:
                    telefono = "0000000000"
                    self.nombre_cliente = "Cliente General"
            except Exception as e:
                telefono = "0000000000"
                self.nombre_cliente = "Cliente General"

            # Insertar venta
            sql_venta = """
            INSERT INTO ventas (fecha, total, id_empleado, telefono, forma_pago)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_venta, (fecha, total_venta, id_empleado, telefono, forma_pago))
            id_venta = cursor.lastrowid

            # Detalles de venta e inventario
            for item in self.temp_venta:
                sql_detalle = """
                INSERT INTO detalles_de_venta (codigo_barras, id_venta, cantidad, precio_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s)
                """
                valores_detalle = (
                    item["codigo"], id_venta, item["cantidad"], item["precio"], item["subtotal"]
                )
                cursor.execute(sql_detalle, valores_detalle)

                # Actualizar inventario
                sql_inventario = """
                UPDATE inventario SET cantidad = cantidad - %s WHERE codigo_barras = %s
                """
                cursor.execute(sql_inventario, (item["cantidad"], item["codigo"]))

            conexion.commit()

            # Generar contenido del ticket
            contenido_ticket = self.generar_ticket_contenido(total_venta, id_venta, forma_pago)  # Asegúrate de pasar forma_pago

            # Mostrar ticket en ventana
            self.mostrar_ticket(contenido_ticket)

            wx.MessageBox(f"Venta realizada exitosamente. Cliente: {self.nombre_cliente}", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.Close()
        except Exception as e:
            conexion.rollback()
            wx.MessageBox(f"Error al realizar la venta:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def generar_ticket_contenido(self, total_venta, id_venta, forma_pago):
        contenido = ""
        contenido += "*" * 40 + "\n"
        contenido += f"{'TIENDA PITICO':^40}\n"
        contenido += "*" * 40 + "\n\n"

        contenido += f"Fecha: {datetime.now().strftime('%d/%m/%Y')}\n"
        contenido += f"Hora: {datetime.now().strftime('%H:%M')}\n"
        contenido += f"Cliente: {self.nombre_cliente}\n"
        contenido += f"Número de Venta: {id_venta}\n"
        contenido += "-" * 40 + "\n"

        contenido += f"{'Cant.':<5} {'Producto':<25} {'Precio':>10} {'Importe':>10}\n"
        contenido += "-" * 40 + "\n"

        for idx, item in enumerate(self.temp_venta, start=1):
            contenido += f"{item['cantidad']:<5} {item['nombre'][:25]:<25} ${item['precio']:.2f} ${item['subtotal']:.2f}\n"

        contenido += "-" * 40 + "\n"
        contenido += f"{'Total:':<30}${total_venta:.2f}\n"
        contenido += f"Forma de Pago: {forma_pago}\n"
        contenido += "-" * 40 + "\n"
        contenido += f"{'Gracias por su compra':^40}\n"
        contenido += f"{'Vuelva pronto':^40}\n"
        contenido += "*" * 40 + "\n"

        return contenido

    def mostrar_ticket(self, contenido):
        """Muestra el ticket en una ventana modal."""
        ticket_frame = TicketFrame(self, "Ticket de Venta", contenido)
        ticket_frame.ShowModal()
        ticket_frame.Destroy()

