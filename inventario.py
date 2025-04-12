#Tienda Pitico 
#MARISA RIOS DE PAZ S4A

import wx

app = wx.App() #crear la app

#Ventana Inventario
ventana4 = wx.Frame(None, title='Inventario', size=(500, 400))
panel = wx.Panel(ventana4) 

titulo = wx.StaticText(panel, label="Inventario", pos=(180, 30))
fuente_titulo = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
titulo.SetFont(fuente_titulo)

# Campos del formulario
wx.StaticText(panel, label="Codigo de barras:", pos=(50, 100))
codigo_barras_entry = wx.TextCtrl(panel, pos=(180, 100), size=(200, -1))
codigo_barras_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Cantidad:", pos=(50, 140))
cantidad_entry = wx.TextCtrl(panel, pos=(180, 140), size=(200, -1))
cantidad_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Fecha de actualización:", pos=(50, 180))
fecha_actualizacion_entry = wx.TextCtrl(panel, pos=(180, 180), size=(200, -1))
fecha_actualizacion_entry.SetBackgroundColour("light gray")

#Botones
boton_ancho = 100
espaciado = 10
total_botones = 4 * boton_ancho + 3 * espaciado
inicio_x = (500 - total_botones) // 2
y_botones = 240

boton_crear = wx.Button(panel, label="Crear", pos=(inicio_x, y_botones), size=(boton_ancho, 30))
boton_buscar = wx.Button(panel, label="Buscar", pos=(inicio_x + (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
boton_actualizar = wx.Button(panel, label="Actualizar", pos=(inicio_x + 2 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
boton_eliminar = wx.Button(panel, label="Eliminar", pos=(inicio_x + 3 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))

ventana4.Show()

app.MainLoop()