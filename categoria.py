#Tienda Pitico 
#MARISA RIOS DE PAZ S4A

import wx

# Crear la app
app = wx.App()

# Crear ventana categoria
ventana1 = wx.Frame(None, title='Categorías', size=(500, 400))
panel = wx.Panel(ventana1)

# Título
titulo = wx.StaticText(panel, label="Categorías", pos=(180, 30))
fuente_titulo = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
titulo.SetFont(fuente_titulo)

# Campos del formulario
wx.StaticText(panel, label="Id Categoría:", pos=(50, 100))
id_categoria_entry = wx.TextCtrl(panel, pos=(180, 100), size=(200, -1))
id_categoria_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Nombre:", pos=(50, 140))
nombre_entry = wx.TextCtrl(panel, pos=(180, 140), size=(200, -1))
nombre_entry.SetBackgroundColour("light gray")

# Botones
boton_ancho = 100
espaciado = 10
total_botones = 4 * boton_ancho + 3 * espaciado
inicio_x = (500 - total_botones) // 2
y_botones = 220

boton_crear = wx.Button(panel, label="Crear", pos=(inicio_x, y_botones), size=(boton_ancho, 30))
boton_buscar = wx.Button(panel, label="Buscar", pos=(inicio_x + (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
boton_actualizar = wx.Button(panel, label="Actualizar", pos=(inicio_x + 2 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
boton_eliminar = wx.Button(panel, label="Eliminar", pos=(inicio_x + 3 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))

ventana1.Show() # Mostrar ventana categoria
app.MainLoop()