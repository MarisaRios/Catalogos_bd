#Tienda Pitico 
#MARISA RIOS DE PAZ S4A

import wx
from db import conexion, cursor

def crear_categoria(event):
    id_categoria = id_categoria_entry.GetValue()
    nombre = nombre_entry.GetValue()

    try:
        sql = "INSERT INTO categoria (id_categoria, nombre) VALUES (%s, %s)"
        valores = (id_categoria, nombre)
        cursor.execute(sql, valores)
        conexion.commit()
        wx.MessageBox("Categoría creada exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Error al crear categoría:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

def buscar_categoria(event):
    id_categoria = id_categoria_entry.GetValue()

    try:
        sql = "SELECT nombre FROM categoria WHERE id_categoria = %s"
        cursor.execute(sql, (id_categoria,))
        resultado = cursor.fetchone()
        if resultado:
            nombre_entry.SetValue(resultado[0])
        else:
            wx.MessageBox("Categoría no encontrada", "Aviso", wx.OK | wx.ICON_WARNING)
    except Exception as e:
        wx.MessageBox(f"Error al buscar categoría:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

def actualizar_categoria(event):
    id_categoria = id_categoria_entry.GetValue()
    nombre = nombre_entry.GetValue()

    try:
        sql = "UPDATE categoria SET nombre = %s WHERE id_categoria = %s"
        valores = (nombre, id_categoria)
        cursor.execute(sql, valores)
        conexion.commit()
        wx.MessageBox("Categoría actualizada correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Error al actualizar categoría:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

def eliminar_categoria(event):
    id_categoria = id_categoria_entry.GetValue()

    try:
        sql = "DELETE FROM categoria WHERE id_categoria = %s"
        cursor.execute(sql, (id_categoria,))
        conexion.commit()
        wx.MessageBox("Categoría eliminada", "Éxito", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Error al eliminar categoría:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

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

# Conectar botones con funciones
boton_crear.Bind(wx.EVT_BUTTON, crear_categoria)
boton_buscar.Bind(wx.EVT_BUTTON, buscar_categoria)
boton_actualizar.Bind(wx.EVT_BUTTON, actualizar_categoria)
boton_eliminar.Bind(wx.EVT_BUTTON, eliminar_categoria)

ventana1.Show() # Mostrar ventana categoria
app.MainLoop()