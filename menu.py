# menu.py
import wx
import wx.lib.buttons as buttons
from datetime import datetime
import os

# Importar ventanas (ajusta según tu estructura)
from articulos import ArticuloFrame
from categoria import CategoriaFrame
from clientes import ClienteFrame
from empleados import EmpleadoFrame
from proveedor import ProveedorFrame
from inventario import InventarioFrame
from venta import VentaFrame
from compra import CompraFrame


class MenuPrincipal(wx.Frame):
    def __init__(self, parent=None, nombre_usuario=""):
        super().__init__(parent=None, title="Tienda Pitico - Punto de Venta", size=(1200, 670))
        self.nombre_usuario = nombre_usuario
        self.SetBackgroundColour(wx.Colour(202, 225, 255))  # Azul muy claro

        # Panel principal
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(240, 248, 255))

        # Crear la interfaz
        self.crear_barra_superior(panel)
        self.crear_area_principal(panel)
        self.crear_barra_estado(panel)

        # Layout principal
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(self.barra_superior, 0, wx.EXPAND)
        main_sizer.Add(self.area_principal, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.barra_estado, 0, wx.EXPAND)
        panel.SetSizer(main_sizer)

        self.Centre()
        self.Show()

    def crear_barra_superior(self, parent):
        """Crea la barra superior con logo, título y usuario"""
        self.barra_superior = wx.Panel(parent)
        self.barra_superior.SetBackgroundColour(wx.Colour(70, 130, 180))  # Azul profesional
        self.barra_superior.SetMinSize((-1, 80))
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Logo y título
        logo_sizer = wx.BoxSizer(wx.HORIZONTAL)
        logo_bitmap = self.cargar_logo()
        if logo_bitmap:
            logo_ctrl = wx.StaticBitmap(self.barra_superior, bitmap=logo_bitmap)
        else:
            logo_ctrl = wx.StaticText(self.barra_superior, label="🏪")
            logo_ctrl.SetFont(wx.Font(24, wx.DEFAULT, wx.NORMAL, wx.BOLD))
            logo_ctrl.SetForegroundColour(wx.WHITE)
        titulo = wx.StaticText(self.barra_superior, label="Tienda Pitico - Punto de Venta")
        titulo.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        titulo.SetForegroundColour(wx.WHITE)
        logo_sizer.Add(logo_ctrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        logo_sizer.Add(titulo, 0, wx.ALIGN_CENTER_VERTICAL)

        # Información del usuario
        user_sizer = wx.BoxSizer(wx.VERTICAL)
        fecha_actual = datetime.now().strftime("%d/%m/%Y - %H:%M")
        fecha_label = wx.StaticText(self.barra_superior, label=f"Fecha: {fecha_actual}")
        fecha_label.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        fecha_label.SetForegroundColour(wx.WHITE)
        usuario_label = wx.StaticText(self.barra_superior, label=f"Usuario: {self.nombre_usuario}")
        usuario_label.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        usuario_label.SetForegroundColour(wx.WHITE)
        user_sizer.Add(fecha_label, 0, wx.ALIGN_RIGHT)
        user_sizer.Add(usuario_label, 0, wx.ALIGN_RIGHT)

        # Botón salir
        btn_salir = wx.Button(self.barra_superior, label="Salir", size=(80, 35))
        btn_salir.SetBackgroundColour(wx.Colour(220, 20, 60))  # Rojo
        btn_salir.SetForegroundColour(wx.WHITE)
        btn_salir.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        btn_salir.Bind(wx.EVT_BUTTON, self.salir_aplicacion)

        sizer.Add(logo_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 20)
        sizer.AddStretchSpacer()
        sizer.Add(user_sizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 20)
        sizer.Add(btn_salir, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 20)

        self.barra_superior.SetSizer(sizer)

    def crear_area_principal(self, parent):
        """Crea el área principal con los botones del menú"""
        self.area_principal = wx.Panel(parent)
        self.area_principal.SetBackgroundColour(wx.Colour(240, 248, 255))
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Título del menú principal
        titulo_menu = wx.StaticText(self.area_principal, label="MENÚ PRINCIPAL")
        titulo_menu.SetFont(wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        titulo_menu.SetForegroundColour(wx.Colour(25, 25, 112))  # Azul marino
        subtitulo = wx.StaticText(self.area_principal, label="Seleccione una opción para continuar")
        subtitulo.SetFont(wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        subtitulo.SetForegroundColour(wx.Colour(70, 130, 180))

        # Contenedor de botones
        botones_panel = wx.Panel(self.area_principal)
        botones_panel.SetBackgroundColour(wx.Colour(240, 248, 255))

        grid_sizer = wx.GridSizer(rows=3, cols=3, vgap=15, hgap=15)

        botones_info = [
            ("📦 Gestionar\nArtículos", self.abrir_articulos, wx.Colour(70, 130, 180)),
            ("📂 Gestionar\nCategorías", self.abrir_categorias, wx.Colour(70, 130, 180)),
            ("👥 Gestionar\nClientes", self.abrir_clientes, wx.Colour(70, 130, 180)),
            ("👤 Gestionar\nEmpleados", self.abrir_empleados, wx.Colour(70, 130, 180)),
            ("🏭 Gestionar\nProveedores", self.abrir_proveedores, wx.Colour(70, 130, 180)),
            ("📊 Gestionar\nInventario", self.abrir_inventario, wx.Colour(70, 130, 180)),
            ("💰 Realizar\nVenta", self.abrir_ventas, wx.Colour(34, 139, 34)),  # Verde para ventas
            ("🛒 Realizar\nCompra", self.abrir_compras, wx.Colour(255, 140, 0)),  # Naranja para compras
            ("", None, None)  # Espacio vacío
        ]

        for texto, evento, color in botones_info:
            if texto:
                boton = wx.Button(botones_panel, label=texto, size=(180, 100))
                boton.SetFont(wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD))
                boton.SetBackgroundColour(color)
                boton.SetForegroundColour(wx.WHITE)
                boton.Bind(wx.EVT_ENTER_WINDOW, lambda evt, b=boton, c=color: self.on_hover_enter(evt, b, c))
                boton.Bind(wx.EVT_LEAVE_WINDOW, lambda evt, b=boton, c=color: self.on_hover_leave(evt, b, c))
                if evento:
                    boton.Bind(wx.EVT_BUTTON, evento)
                grid_sizer.Add(boton, 0, wx.EXPAND)
            else:
                grid_sizer.Add((0, 0))

        botones_panel.SetSizer(grid_sizer)

        sizer.Add(titulo_menu, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 20)
        sizer.Add(subtitulo, 0, wx.ALIGN_CENTER | wx.BOTTOM, 30)
        sizer.Add(botones_panel, 1, wx.ALIGN_CENTER)
        self.area_principal.SetSizer(sizer)

    def crear_barra_estado(self, parent):
        """Crea la barra de estado inferior"""
        self.barra_estado = wx.Panel(parent)
        self.barra_estado.SetBackgroundColour(wx.Colour(176, 196, 222))  # Azul claro
        self.barra_estado.SetMinSize((-1, 30))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        estado_text = wx.StaticText(self.barra_estado, label="Tienda Pitico")
        estado_text.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        estado_text.SetForegroundColour(wx.Colour(25, 25, 112))
        version_text = wx.StaticText(self.barra_estado, label="v1.0 - MARISA RIOS DE PAZ S4A")
        version_text.SetFont(wx.Font(9, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        version_text.SetForegroundColour(wx.Colour(25, 25, 112))
        sizer.Add(estado_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        sizer.AddStretchSpacer()
        sizer.Add(version_text, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 10)
        self.barra_estado.SetSizer(sizer)

    def cargar_logo(self):
        """Carga el logo de la tienda desde archivo"""
        rutas_logo = ["pitico.png"]
        for ruta in rutas_logo:
            if os.path.exists(ruta):
                try:
                    imagen = wx.Image(ruta, wx.BITMAP_TYPE_ANY)
                    imagen = imagen.Scale(48, 48, wx.IMAGE_QUALITY_HIGH)
                    return wx.Bitmap(imagen)
                except Exception as e:
                    print(f"Error cargando logo desde {ruta}: {e}")
        print("Logo no encontrado. Coloca tu logo como 'pitico.png' en la carpeta del programa")
        return None

    def on_hover_enter(self, event, boton, color_original):
        r, g, b = color_original.Red(), color_original.Green(), color_original.Blue()
        color_hover = wx.Colour(min(255, r + 30), min(255, g + 30), min(255, b + 30))
        boton.SetBackgroundColour(color_hover)
        boton.Refresh()

    def on_hover_leave(self, event, boton, color_original):
        boton.SetBackgroundColour(color_original)
        boton.Refresh()

    def salir_aplicacion(self, event):
        dlg = wx.MessageDialog(self, "¿Está seguro que desea salir del sistema?",
                              "Confirmar Salida", wx.YES_NO | wx.ICON_QUESTION)
        if dlg.ShowModal() == wx.ID_YES:
            self.Close()
        dlg.Destroy()

    # Métodos para abrir las ventanas
    def abrir_articulos(self, event):
        ventana = ArticuloFrame(self)
        ventana.Show()

    def abrir_categorias(self, event):
        ventana = CategoriaFrame(self)
        ventana.Show()

    def abrir_clientes(self, event):
        ventana = ClienteFrame(self)
        ventana.Show()

    def abrir_empleados(self, event):
        ventana = EmpleadoFrame(self)
        ventana.Show()

    def abrir_proveedores(self, event):
        ventana = ProveedorFrame(self)
        ventana.Show()

    def abrir_inventario(self, event):
        ventana = InventarioFrame(self)
        ventana.Show()

    def abrir_ventas(self, event):
        ventana = VentaFrame(self)
        ventana.Show()

    def abrir_compras(self, event):
        ventana = CompraFrame(self)
        ventana.Show()