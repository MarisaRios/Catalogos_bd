import wx
from db import conexion, cursor


class ArticuloFrame(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title='Artículos', size=(900, 600))
        self.panel = wx.Panel(self)
        self.existencia_original = None 
        self.crear_interfaz()
        self.Centre()

    def crear_interfaz(self):
        # Título
        titulo = wx.StaticText(self.panel, label="Artículos", pos=(350, 30))
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

        # Agregar lista de artículos
        self.lista_articulos = wx.ListCtrl(
            self.panel,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN,
            pos=(50, 420),
            size=(750, 150)
        )
        self.lista_articulos.InsertColumn(0, "Código de Barras", width=150)
        self.lista_articulos.InsertColumn(1, "Nombre", width=200)
        self.lista_articulos.InsertColumn(2, "Precio", width=100)
        self.lista_articulos.InsertColumn(3, "Existencia", width=100)
        self.lista_articulos.InsertColumn(4, "Unidad", width=100)
        self.lista_articulos.InsertColumn(5, "Descripción", width=200)
        self.lista_articulos.InsertColumn(6, "ID Categoría", width=100)

        # Evento un click para seleccionar artículo de la lista
        self.lista_articulos.Bind(wx.EVT_LIST_ITEM_SELECTED, self.seleccionar_articulo_de_lista)

        # Cargar datos iniciales en la lista
        self.cargar_lista_articulos()

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
            self.limpiar_campos()
            self.cargar_lista_articulos()
        except Exception as e:
            wx.MessageBox(f"Error al crear artículo:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def buscar_articulo(self, event):
        codigo_barras = self.codigo_barras_entry.GetValue().strip()
        nombre = self.nombre_entry.GetValue().strip()
        id_categoria = self.id_categoria_entry.GetValue().strip()

        condiciones = []
        valores = []

        if codigo_barras:
            condiciones.append("codigo_barras = %s")
            valores.append(codigo_barras)
        if nombre:
            condiciones.append("nombre LIKE %s")
            valores.append(f"%{nombre}%")
        if id_categoria:
            condiciones.append("id_categoria = %s")
            valores.append(id_categoria)

        sql = "SELECT codigo_barras, nombre, precio, existencia, unidad, descripcion, id_categoria FROM articulos"
        if condiciones:
            sql += " WHERE " + " AND ".join(condiciones)

        try:
            cursor.execute(sql, tuple(valores))
            resultados = cursor.fetchall()

            self.lista_articulos.DeleteAllItems()
            self.limpiar_campos()

            for idx, row in enumerate(resultados):
                self.lista_articulos.InsertItem(idx, str(row[0]))
                self.lista_articulos.SetItem(idx, 1, row[1])
                self.lista_articulos.SetItem(idx, 2, str(row[2]))
                self.lista_articulos.SetItem(idx, 3, str(row[3]))
                self.lista_articulos.SetItem(idx, 4, row[4])
                self.lista_articulos.SetItem(idx, 5, row[5])
                self.lista_articulos.SetItem(idx, 6, str(row[6]))

            if len(resultados) == 1:
                row = resultados[0]
                self.codigo_barras_entry.SetValue(str(row[0]))
                self.nombre_entry.SetValue(row[1])
                self.precio_entry.SetValue(str(row[2]))
                self.existencia_entry.SetValue(str(row[3]))
                self.existencia_original = str(row[3])
                self.unidad_entry.SetValue(row[4] or "")
                self.descripcion_entry.SetValue(row[5] or "")
                self.id_categoria_entry.SetValue(str(row[6]))
            elif len(resultados) > 1:
                wx.MessageBox("Se encontraron múltiples artículos. Seleccione uno de la lista.", "Información", wx.OK | wx.ICON_INFORMATION)
            elif not resultados:
                wx.MessageBox("No se encontraron artículos", "Aviso", wx.OK | wx.ICON_WARNING)

        except Exception as e:
            wx.MessageBox(f"Error al buscar artículo:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def seleccionar_articulo_de_lista(self, event):
        index = event.GetIndex()
        codigo_barras = self.lista_articulos.GetItemText(index, 0)

        try:
            sql = "SELECT nombre, precio, existencia, unidad, descripcion, id_categoria FROM articulos WHERE codigo_barras = %s"
            cursor.execute(sql, (codigo_barras,))
            resultado = cursor.fetchone()

            if resultado:
                self.codigo_barras_entry.SetValue(codigo_barras)
                self.nombre_entry.SetValue(resultado[0])
                self.precio_entry.SetValue(str(resultado[1]))
                self.existencia_entry.SetValue(str(resultado[2]))
                self.existencia_original = str(resultado[2])
                self.unidad_entry.SetValue(resultado[3] or "")
                self.descripcion_entry.SetValue(resultado[4] or "")
                self.id_categoria_entry.SetValue(str(resultado[5]))
        except Exception as e:
            wx.MessageBox(f"Error al seleccionar artículo:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def actualizar_articulo(self, event):
        codigo_barras = self.codigo_barras_entry.GetValue()
        nombre = self.nombre_entry.GetValue()
        precio = self.precio_entry.GetValue()
        existencia = self.existencia_entry.GetValue()
        unidad = self.unidad_entry.GetValue()
        descripcion = self.descripcion_entry.GetValue()
        id_categoria = self.id_categoria_entry.GetValue()

        if not existencia.strip():
            wx.MessageBox("El campo 'Existencia' no puede estar vacío.", "Error", wx.OK | wx.ICON_ERROR)
            return

        if existencia == self.existencia_original:
            wx.MessageBox("Debe modificar el campo 'Existencia' para realizar una actualización.", "Advertencia", wx.OK | wx.ICON_WARNING)
            return

        try:
            sql = """UPDATE articulos SET nombre = %s, precio = %s, existencia = %s, unidad = %s, descripcion = %s, 
                    id_categoria = %s WHERE codigo_barras = %s"""
            valores = (nombre, float(precio), int(existencia), unidad, descripcion, int(id_categoria), codigo_barras)
            cursor.execute(sql, valores)
            conexion.commit()
            wx.MessageBox("Artículo actualizado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.limpiar_campos()
            self.cargar_lista_articulos()
        except Exception as e:
            wx.MessageBox(f"Error al actualizar artículo:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def eliminar_articulo(self, event):
        codigo_barras = self.codigo_barras_entry.GetValue()

        try:
            sql = "DELETE FROM articulos WHERE codigo_barras = %s"
            cursor.execute(sql, (codigo_barras,))
            conexion.commit()
            wx.MessageBox("Artículo eliminado", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.limpiar_campos()
            self.cargar_lista_articulos()
        except Exception as e:
            wx.MessageBox(f"Error al eliminar artículo:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def cargar_lista_articulos(self):
        self.lista_articulos.DeleteAllItems()
        try:
            sql = "SELECT codigo_barras, nombre, precio, existencia, unidad, descripcion, id_categoria FROM articulos"
            cursor.execute(sql)
            resultados = cursor.fetchall()

            for idx, row in enumerate(resultados):
                self.lista_articulos.InsertItem(idx, str(row[0]))
                self.lista_articulos.SetItem(idx, 1, row[1])
                self.lista_articulos.SetItem(idx, 2, str(row[2]))
                self.lista_articulos.SetItem(idx, 3, str(row[3]))
                self.lista_articulos.SetItem(idx, 4, row[4])
                self.lista_articulos.SetItem(idx, 5, row[5])
                self.lista_articulos.SetItem(idx, 6, str(row[6]))
        except Exception as e:
            wx.MessageBox(f"Error al cargar lista de artículos:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def limpiar_campos(self):
        self.codigo_barras_entry.Clear()
        self.nombre_entry.Clear()
        self.precio_entry.Clear()
        self.existencia_entry.Clear()
        self.unidad_entry.Clear()
        self.descripcion_entry.Clear()
        self.id_categoria_entry.Clear()
