# Punto de Venta - Tienda Pitico
# MARISA RIOS DE PAZ S4A

import wx
from datetime import datetime
from db import conexion, cursor


class TicketFrame(wx.Dialog):
    """Ventana que muestra el ticket formateado como una ventana modal - Versión mejorada"""
    def __init__(self, parent, titulo, contenido):
        super().__init__(parent, title=titulo, size=(450, 650))
        self.SetBackgroundColour(wx.Colour(255, 255, 255))  # Fondo blanco

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Título del ticket
        titulo_ticket = wx.StaticText(panel, label="🛒TIENDA PITICO")
        fuente_titulo = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        titulo_ticket.SetFont(fuente_titulo)
        titulo_ticket.SetForegroundColour(wx.BLACK)

        # Contenido del ticket 
        texto_contenido = wx.TextCtrl(
            panel,
            value=contenido,
            style=wx.TE_MULTILINE | wx.TE_READONLY,
            size=(400, 520)
        )
        
        fuente_mono = wx.Font(10, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL)
        texto_contenido.SetFont(fuente_mono)
        texto_contenido.SetBackgroundColour(wx.WHITE)
        texto_contenido.SetForegroundColour(wx.BLACK)

        # Botones
        sizer_botones = wx.BoxSizer(wx.HORIZONTAL)
        
        boton_cerrar = wx.Button(panel, label="Cerrar", size=(80, 30))
        boton_cerrar.SetBackgroundColour(wx.Colour(178, 34, 34))
        boton_cerrar.SetForegroundColour(wx.WHITE)
        boton_cerrar.Bind(wx.EVT_BUTTON, self.on_cerrar)

        sizer_botones.Add(boton_cerrar, 0)

        # Layout
        sizer.Add(titulo_ticket, 0, wx.ALIGN_CENTER | wx.TOP, 15)
        sizer.Add(texto_contenido, 1, wx.EXPAND | wx.ALL, 15)
        sizer.Add(sizer_botones, 0, wx.ALIGN_CENTER | wx.BOTTOM, 15)
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

        # Consultar información del artículo y su inventario
        sql = """
        SELECT a.nombre, a.precio, i.cantidad AS cantidad_inventario 
        FROM articulos a
        JOIN inventario i ON a.codigo_barras = i.codigo_barras
        WHERE a.codigo_barras = %s
        """
        cursor.execute(sql, (codigo,))
        resultado = cursor.fetchone()

        if not resultado:
            wx.MessageBox("Artículo no encontrado o sin inventario.", "Error", wx.OK | wx.ICON_ERROR)
            return

        nombre, precio, cantidad_inventario = resultado

        # Verificar si hay suficiente inventario
        if cantidad > cantidad_inventario:
            wx.MessageBox(f"No hay suficiente inventario. Solo hay {cantidad_inventario} unidades disponibles.",
                        "Inventario Insuficiente", wx.OK | wx.ICON_WARNING)
            return

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
        monto_recibido = None
        cambio = 0
        
        if forma_pago == "Efectivo":
            while True:
                dlg_monto = wx.TextEntryDialog(self, "Ingrese el monto con el que paga el cliente:", 
                                            "Pago en Efectivo", "")
                if dlg_monto.ShowModal() == wx.ID_OK:
                    try:
                        monto_recibido = float(dlg_monto.GetValue())
                        total_venta = sum(item["subtotal"] for item in self.temp_venta)
                        if monto_recibido < total_venta:
                            wx.MessageBox("El monto recibido es menor al total. Por favor, ingrese un monto válido.",
                                        "Monto Insuficiente", wx.OK | wx.ICON_ERROR)
                        else:
                            cambio = monto_recibido - total_venta
                            break
                    except ValueError:
                        wx.MessageBox("Por favor, ingrese un monto válido.", "Error", wx.OK | wx.ICON_ERROR)
                else:
                    return  # El usuario canceló el ingreso del monto
        
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
            contenido_ticket = self.generar_ticket_contenido(
                total_venta, id_venta, forma_pago, monto_recibido, cambio
            )
            
            # Mostrar ticket en ventana
            self.mostrar_ticket(contenido_ticket)
            wx.MessageBox(f"Venta realizada exitosamente. Cliente: {self.nombre_cliente}", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.Close()
        except Exception as e:
            conexion.rollback()
            wx.MessageBox(f"Error al realizar la venta:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def generar_ticket_contenido(self, total_venta, id_venta, forma_pago, monto_recibido=None, cambio=None):
        contenido = ""
        contenido += "*" * 40 + "\n"
        contenido += f"{'🛒TIENDA PITICO':^40}\n"
        contenido += "*" * 40 + "\n\n"

        contenido += f"Fecha: {datetime.now().strftime('%d/%m/%Y')}\n"
        contenido += f"Hora: {datetime.now().strftime('%H:%M')}\n"
        contenido += f"Cliente: {self.nombre_cliente}\n"
        contenido += f"Número de Venta: {id_venta}\n"
        contenido += "-" * 40 + "\n\n"  # Línea extra para separación

        # Encabezado de productos con mejor formato
        contenido += f"{'Cant.':<6}{'Producto':<18}{'Precio':>8}{'Importe':>8}\n"
        contenido += "-" * 40 + "\n"

        # Productos con mejor espaciado
        for idx, item in enumerate(self.temp_venta, start=1):
            # Truncar nombre del producto si es muy largo
            nombre_producto = item['nombre'][:16] if len(item['nombre']) > 16 else item['nombre']
            
            contenido += f"{item['cantidad']:<6}{nombre_producto:<18}${item['precio']:>6.2f}${item['subtotal']:>7.2f}\n"
            contenido += "\n"  # Línea vacía entre productos para mejor separación

        contenido += "-" * 40 + "\n"
        contenido += f"{'TOTAL:':.<25}${total_venta:>10.2f}\n"
        if forma_pago == "Efectivo" and monto_recibido is not None:
            contenido += f"Forma de Pago: {forma_pago} ($    {monto_recibido:.2f})\n"
            if cambio > 0:
                contenido += f"Cambio: ${cambio:.2f}\n"
        else:
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

