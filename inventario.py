#Tienda Pitico 
#MARISA RIOS DE PAZ S4A

import wx
from datetime import datetime
from db import conexion, cursor  

def crear_inventario(event):
    codigo = codigo_barras_entry.GetValue()
    cantidad = cantidad_entry.GetValue()
    fecha = fecha_actualizacion_entry.GetValue()

    if fecha.strip() == "":
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        sql = "INSERT INTO inventario (codigo_barras, cantidad, fecha_actualizacion) VALUES (%s, %s, %s)"
        valores = (codigo, cantidad, fecha)
        cursor.execute(sql, valores)
        conexion.commit()
        wx.MessageBox("Inventario creado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Error al crear inventario:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

def buscar_inventario(event):
    codigo = codigo_barras_entry.GetValue()

    try:
        sql = "SELECT cantidad, fecha_actualizacion FROM inventario WHERE codigo_barras = %s"
        cursor.execute(sql, (codigo,))
        resultado = cursor.fetchone()
        if resultado:
            cantidad_entry.SetValue(str(resultado[0]))
            fecha_actualizacion_entry.SetValue(str(resultado[1]))
        else:
            wx.MessageBox("Inventario no encontrado", "Aviso", wx.OK | wx.ICON_WARNING)
    except Exception as e:
        wx.MessageBox(f"Error al buscar:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

def actualizar_inventario(event):
    codigo = codigo_barras_entry.GetValue()
    cantidad = cantidad_entry.GetValue()
    fecha = fecha_actualizacion_entry.GetValue()

    if fecha.strip() == "":
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        sql = "UPDATE inventario SET cantidad = %s, fecha_actualizacion = %s WHERE codigo_barras = %s"
        valores = (cantidad, fecha, codigo)
        cursor.execute(sql, valores)
        conexion.commit()
        wx.MessageBox("Inventario actualizado", "Éxito", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Error al actualizar:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

def eliminar_inventario(event):
    codigo = codigo_barras_entry.GetValue()

    try:
        sql = "DELETE FROM inventario WHERE codigo_barras = %s"
        cursor.execute(sql, (codigo,))
        conexion.commit()
        wx.MessageBox("Inventario eliminado", "Éxito", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Error al eliminar:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

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

boton_crear.Bind(wx.EVT_BUTTON, crear_inventario)
boton_buscar.Bind(wx.EVT_BUTTON, buscar_inventario)
boton_actualizar.Bind(wx.EVT_BUTTON, actualizar_inventario)
boton_eliminar.Bind(wx.EVT_BUTTON, eliminar_inventario)

ventana4.Show()

app.MainLoop()