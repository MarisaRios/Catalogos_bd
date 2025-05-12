#Tienda Pitico 
#MARISA RIOS DE PAZ S4A
import wx
from db import conexion, cursor

def crear_proveedor(event):
    id_proveedor = id_proveedor_entry.GetValue()
    nombre = nombre_entry.GetValue()
    contacto = contacto_entry.GetValue()
    telefono = telefono_entry.GetValue()
    email = email_entry.GetValue()
    direccion = direccion_entry.GetValue()

    try:
        sql = "INSERT INTO proveedor (id_proveedor, nombre, contacto, telefono, email, direccion) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (id_proveedor, nombre, contacto, telefono, email, direccion)
        cursor.execute(sql, valores)
        conexion.commit()
        wx.MessageBox("Proveedor creado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Error al crear proveedor:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

def buscar_proveedor(event):
    id_proveedor = id_proveedor_entry.GetValue()
    try:
        sql = "SELECT nombre, contacto, telefono, email, direccion FROM proveedor WHERE id_proveedor = %s"
        cursor.execute(sql, (id_proveedor,))
        resultado = cursor.fetchone()
        if resultado:
            nombre_entry.SetValue(resultado[0])
            contacto_entry.SetValue(resultado[1])
            telefono_entry.SetValue(resultado[2])
            email_entry.SetValue(resultado[3])
            direccion_entry.SetValue(resultado[4])
        else:
            wx.MessageBox("Proveedor no encontrado", "Aviso", wx.OK | wx.ICON_WARNING)
    except Exception as e:
        wx.MessageBox(f"Error al buscar proveedor:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

def actualizar_proveedor(event):
    id_proveedor = id_proveedor_entry.GetValue()
    nombre = nombre_entry.GetValue()
    contacto = contacto_entry.GetValue()
    telefono = telefono_entry.GetValue()
    email = email_entry.GetValue()
    direccion = direccion_entry.GetValue()

    try:
        sql = "UPDATE proveedor SET nombre=%s, contacto=%s, telefono=%s, email=%s, direccion=%s WHERE id_proveedor=%s"
        valores = (nombre, contacto, telefono, email, direccion, id_proveedor)
        cursor.execute(sql, valores)
        conexion.commit()
        wx.MessageBox("Proveedor actualizado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Error al actualizar proveedor:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

def eliminar_proveedor(event):
    id_proveedor = id_proveedor_entry.GetValue()
    try:
        sql = "DELETE FROM proveedor WHERE id_proveedor = %s"
        cursor.execute(sql, (id_proveedor,))
        conexion.commit()
        wx.MessageBox("Proveedor eliminado", "Éxito", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Error al eliminar proveedor:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)


app = wx.App() #crear la app

#Ventana PROVEEDOR
ventana5 = wx.Frame(None, title='Proveedor', size=(500, 500))
panel = wx.Panel(ventana5) 

titulo = wx.StaticText(panel, label="Proveedor", pos=(180, 30))
fuente_titulo = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
titulo.SetFont(fuente_titulo)

# Campos del formulario
wx.StaticText(panel, label="Id Proveedor:", pos=(50, 100))
id_proveedor_entry = wx.TextCtrl(panel, pos=(180, 100), size=(200, -1))
id_proveedor_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Nombre:", pos=(50, 140))
nombre_entry = wx.TextCtrl(panel, pos=(180, 140), size=(200, -1))
nombre_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Contacto:", pos=(50, 180))
contacto_entry = wx.TextCtrl(panel, pos=(180, 180), size=(200, -1))
contacto_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Telefono:", pos=(50, 220))
telefono_entry = wx.TextCtrl(panel, pos=(180, 220), size=(200, -1))
telefono_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Email:", pos=(50, 260))
email_entry = wx.TextCtrl(panel, pos=(180, 260), size=(200, -1))
email_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Dirección:", pos=(50, 300))
direccion_entry = wx.TextCtrl(panel, pos=(180, 300), size=(200, -1))
direccion_entry.SetBackgroundColour("light gray")

# Botones
boton_ancho = 100
espaciado = 10
total_botones = 4 * boton_ancho + 3 * espaciado
inicio_x = (500 - total_botones) // 2
y_botones = 355

boton_crear = wx.Button(panel, label="Crear", pos=(inicio_x, y_botones), size=(boton_ancho, 30))
boton_buscar = wx.Button(panel, label="Buscar", pos=(inicio_x + (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
boton_actualizar = wx.Button(panel, label="Actualizar", pos=(inicio_x + 2 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
boton_eliminar = wx.Button(panel, label="Eliminar", pos=(inicio_x + 3 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))

boton_crear.Bind(wx.EVT_BUTTON, crear_proveedor)
boton_buscar.Bind(wx.EVT_BUTTON, buscar_proveedor)
boton_actualizar.Bind(wx.EVT_BUTTON, actualizar_proveedor)
boton_eliminar.Bind(wx.EVT_BUTTON, eliminar_proveedor)

ventana5.Show()

app.MainLoop()