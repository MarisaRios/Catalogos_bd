import wx
from db import conexion, cursor


class CategoriaFrame(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title='Categorías', size=(700, 500))
        self.panel = wx.Panel(self)

        self.crear_interfaz()
        self.Centre()

    def crear_interfaz(self):
        # Título
        titulo = wx.StaticText(self.panel, label="Categorías", pos=(300, 30))
        fuente_titulo = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        titulo.SetFont(fuente_titulo)

        # Campos del formulario
        wx.StaticText(self.panel, label="Id Categoría:", pos=(50, 80))
        self.id_categoria_entry = wx.TextCtrl(self.panel, pos=(180, 80), size=(200, -1))
        self.id_categoria_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Nombre:", pos=(50, 120))
        self.nombre_entry = wx.TextCtrl(self.panel, pos=(180, 120), size=(200, -1))
        self.nombre_entry.SetBackgroundColour("light gray")

        # Botones
        boton_ancho = 100
        espaciado = 10
        total_botones = 4 * boton_ancho + 3 * espaciado
        inicio_x = (700 - total_botones) // 2
        y_botones = 180

        self.boton_crear = wx.Button(self.panel, label="Crear", pos=(inicio_x, y_botones), size=(boton_ancho, 30))
        self.boton_buscar = wx.Button(self.panel, label="Buscar", pos=(inicio_x + (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
        self.boton_actualizar = wx.Button(self.panel, label="Actualizar", pos=(inicio_x + 2 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
        self.boton_eliminar = wx.Button(self.panel, label="Eliminar", pos=(inicio_x + 3 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))

        self.boton_regresar = wx.Button(self.panel, label="Regresar", pos=(20, 20), size=(80, 30))
        self.boton_regresar.SetBackgroundColour(wx.Colour(178, 34, 34))  # Rojo oscuro
        self.boton_regresar.SetForegroundColour(wx.WHITE)
        self.boton_regresar.Bind(wx.EVT_BUTTON, self.volver_menu)

        # Asignar eventos
        self.boton_crear.Bind(wx.EVT_BUTTON, self.crear_categoria)
        self.boton_buscar.Bind(wx.EVT_BUTTON, self.buscar_categoria)
        self.boton_actualizar.Bind(wx.EVT_BUTTON, self.actualizar_categoria)
        self.boton_eliminar.Bind(wx.EVT_BUTTON, self.eliminar_categoria)

        # Lista de categorías
        self.lista_categorias = wx.ListCtrl(
            self.panel,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN,
            pos=(50, 240),
            size=(600, 200)
        )
        self.lista_categorias.InsertColumn(0, "ID Categoría", width=150)
        self.lista_categorias.InsertColumn(1, "Nombre", width=450)

        # Evento de un click en la lista
        self.lista_categorias.Bind(wx.EVT_LIST_ITEM_SELECTED, self.seleccionar_categoria)

        # Cargar datos iniciales
        self.cargar_lista_categorias()

    def seleccionar_categoria(self, event):
        """Llena los campos cuando se hace doble clic en un elemento de la lista"""
        index = event.GetIndex()
        id_categoria = self.lista_categorias.GetItemText(index, col=0)
        nombre = self.lista_categorias.GetItemText(index, col=1)

        self.id_categoria_entry.SetValue(id_categoria)
        self.nombre_entry.SetValue(nombre)

    def volver_menu(self, event):
        from menu import MenuPrincipal
        frame = MenuPrincipal()
        frame.Show()
        self.Close()

    def crear_categoria(self, event):
        id_categoria = self.id_categoria_entry.GetValue().strip()
        nombre = self.nombre_entry.GetValue().strip()

        if not id_categoria or not nombre:
            wx.MessageBox("Por favor complete todos los campos", "Advertencia", wx.OK | wx.ICON_WARNING)
            return

        try:
            sql = "INSERT INTO categoria (id_categoria, nombre) VALUES (%s, %s)"
            valores = (id_categoria, nombre)
            cursor.execute(sql, valores)
            conexion.commit()
            wx.MessageBox("Categoría creada exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.limpiar_campos()
            self.cargar_lista_categorias()
        except Exception as e:
            wx.MessageBox(f"Error al crear categoría:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def buscar_categoria(self, event):
        id_categoria = self.id_categoria_entry.GetValue().strip()
        nombre = self.nombre_entry.GetValue().strip()

        condiciones = []
        valores = []

        if id_categoria:
            condiciones.append("id_categoria = %s")
            valores.append(id_categoria)
        if nombre:
            condiciones.append("nombre LIKE %s")
            valores.append(f"%{nombre}%")

        sql = "SELECT id_categoria, nombre FROM categoria"
        if condiciones:
            sql += " WHERE " + " AND ".join(condiciones)

        try:
            cursor.execute(sql, tuple(valores))
            resultados = cursor.fetchall()

            self.lista_categorias.DeleteAllItems()

            for idx, row in enumerate(resultados):
                self.lista_categorias.InsertItem(idx, str(row[0]))
                self.lista_categorias.SetItem(idx, 1, row[1])

            if len(resultados) == 1:
                # Llenar automáticamente los campos solo si hay una coincidencia exacta
                self.id_categoria_entry.SetValue(str(resultados[0][0]))  # Convertir a string
                self.nombre_entry.SetValue(resultados[0][1])

            elif not resultados:
                wx.MessageBox("No se encontraron categorías", "Aviso", wx.OK | wx.ICON_WARNING)
        except Exception as e:
            wx.MessageBox(f"Error al buscar categoría:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def actualizar_categoria(self, event):
        id_categoria = self.id_categoria_entry.GetValue().strip()
        nombre = self.nombre_entry.GetValue().strip()

        if not id_categoria:
            wx.MessageBox("Debe ingresar el ID de la categoría a actualizar", "Advertencia", wx.OK | wx.ICON_WARNING)
            return

        try:
            sql = "UPDATE categoria SET nombre = %s WHERE id_categoria = %s"
            valores = (nombre, id_categoria)
            cursor.execute(sql, valores)
            conexion.commit()
            wx.MessageBox("Categoría actualizada correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.limpiar_campos()
            self.cargar_lista_categorias()
        except Exception as e:
            wx.MessageBox(f"Error al actualizar categoría:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def eliminar_categoria(self, event):
        id_categoria = self.id_categoria_entry.GetValue().strip()

        if not id_categoria:
            wx.MessageBox("Debe ingresar el ID de la categoría a eliminar", "Advertencia", wx.OK | wx.ICON_WARNING)
            return

        try:
            sql = "DELETE FROM categoria WHERE id_categoria = %s"
            cursor.execute(sql, (id_categoria,))
            conexion.commit()
            wx.MessageBox("Categoría eliminada", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.limpiar_campos()
            self.cargar_lista_categorias()
        except Exception as e:
            wx.MessageBox(f"Error al eliminar categoría:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def cargar_lista_categorias(self):
        self.lista_categorias.DeleteAllItems()

        try:
            sql = "SELECT id_categoria, nombre FROM categoria"
            cursor.execute(sql)
            resultados = cursor.fetchall()

            for idx, row in enumerate(resultados):
                self.lista_categorias.InsertItem(idx, str(row[0]))  # Convertir a string
                self.lista_categorias.SetItem(idx, 1, row[1])
        except Exception as e:
            wx.MessageBox(f"Error al cargar lista de categorías:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def limpiar_campos(self):
        self.id_categoria_entry.Clear()
        self.nombre_entry.Clear()