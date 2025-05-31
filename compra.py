# Compra - Tienda Pitico
# MARISA RIOS DE PAZ S4A

import wx
from datetime import datetime
from db import conexion, cursor


class CompraFrame(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title="Registrar Compra", size=(950, 680))
        self.panel = wx.Panel(self)
        self.SetBackgroundColour(wx.Colour(245, 245, 245))

        self.articulos_seleccionados = []

        self.crear_interfaz()
        self.Centre()

    def crear_interfaz(self):
        # Título
        titulo = wx.StaticText(self.panel, label="Registrar Compra", pos=(110, 10))
        fuente_titulo = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        titulo.SetFont(fuente_titulo)

        # Botón Regresar
        self.boton_regresar = wx.Button(self.panel, label="Regresar", pos=(20, 20), size=(80, 30))
        self.boton_regresar.SetBackgroundColour(wx.Colour(178, 34, 34))  # Rojo oscuro
        self.boton_regresar.SetForegroundColour(wx.WHITE)
        self.boton_regresar.Bind(wx.EVT_BUTTON, self.volver_menu)

        # Datos del proveedor
        wx.StaticText(self.panel, label="ID Proveedor:", pos=(30, 70))
        self.id_proveedor_entry = wx.TextCtrl(self.panel, pos=(180, 70), size=(200, -1))

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
        self.boton_finalizar = wx.Button(self.panel, label="Finalizar Compra", pos=(650, 500), size=(180, 40))
        self.boton_finalizar.SetBackgroundColour(wx.Colour(66, 133, 244))
        self.boton_finalizar.SetForegroundColour(wx.WHITE)
        self.boton_finalizar.Bind(wx.EVT_BUTTON, self.finalizar_compra)

        # Eventos
        self.boton_agregar.Bind(wx.EVT_BUTTON, self.agregar_articulo)
        self.boton_limpiar.Bind(wx.EVT_BUTTON, self.limpiar_formulario)

    def volver_menu(self, event):
        from menu import MenuPrincipal
        frame = MenuPrincipal()
        frame.Show()
        self.Close()

    def limpiar_formulario(self, event):
        self.id_proveedor_entry.SetValue("")
        self.codigo_barras_entry.SetValue("")
        self.cantidad_entry.SetValue("")
        self.articulos_seleccionados.clear()
        self.lista_articulos.DeleteAllItems()
        self.etiqueta_total.SetLabel("Total: $0.00")

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

        self.articulos_seleccionados.append({
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
        for idx, item in enumerate(self.articulos_seleccionados):
            self.lista_articulos.InsertItem(idx, item["codigo"])
            self.lista_articulos.SetItem(idx, 1, item["nombre"])
            self.lista_articulos.SetItem(idx, 2, f"${item['precio']:.2f}")
            self.lista_articulos.SetItem(idx, 3, str(item["cantidad"]))
            self.lista_articulos.SetItem(idx, 4, f"${item['subtotal']:.2f}")

        total = sum(item["subtotal"] for item in self.articulos_seleccionados)
        self.etiqueta_total.SetLabel(f"Total: ${total:.2f}")

    def eliminar_articulo_seleccionado(self, event):
        index = self.lista_articulos.GetFirstSelected()
        if index == -1:
            wx.MessageBox("Por favor, seleccione un artículo de la lista.", "Advertencia", wx.OK | wx.ICON_WARNING)
            return
        del self.articulos_seleccionados[index]
        self.actualizar_lista_articulos()

    def finalizar_compra(self, event):
        id_proveedor = self.id_proveedor_entry.GetValue().strip()

        if not id_proveedor:
            wx.MessageBox("Debe ingresar ID de proveedor.", "Faltan Datos", wx.OK | wx.ICON_WARNING)
            return

        try:
            id_proveedor = int(id_proveedor)
        except ValueError:
            wx.MessageBox("El ID del proveedor debe ser un número.", "Error", wx.OK | wx.ICON_ERROR)
            return

        if not self.articulos_seleccionados:
            wx.MessageBox("No hay artículos seleccionados para comprar.", "Compra vacía", wx.OK | wx.ICON_WARNING)
            return

        try:
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            total_compra = sum(item["subtotal"] for item in self.articulos_seleccionados)

            # Insertar compra
            sql_compra = """
            INSERT INTO compras (fecha, total, id_proveedor)
            VALUES (%s, %s, %s)
            """
            cursor.execute(sql_compra, (fecha, total_compra, id_proveedor))
            id_compra = cursor.lastrowid

            for item in self.articulos_seleccionados:
                sql_detalle = """
                INSERT INTO detalles_de_compra (codigo_barras, id_compra, cantidad, precio_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s)
                """
                valores_detalle = (item["codigo"], id_compra, item["cantidad"], item["precio"], item["subtotal"])
                cursor.execute(sql_detalle, valores_detalle)

                sql_inventario = """
                UPDATE inventario SET cantidad = cantidad + %s WHERE codigo_barras = %s
                """
                cursor.execute(sql_inventario, (item["cantidad"], item["codigo"]))

            conexion.commit()

            wx.MessageBox(f"Compra realizada exitosamente. Proveedor: {id_proveedor}", "Éxito",
                          wx.OK | wx.ICON_INFORMATION)
            self.Close()
        except Exception as e:
            conexion.rollback()
            wx.MessageBox(f"Error al realizar la compra:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)
