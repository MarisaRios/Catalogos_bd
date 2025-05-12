#Tienda Pitico 
#MARISA RIOS DE PAZ S4A

import wx
from db import conexion, cursor

def crear_cliente(event):
    telefono = telefono_entry.GetValue()
    nombre = nombre_entry.GetValue()
    apellido = apellido_entry.GetValue()
    email = email_entry.GetValue()
    direccion = direccion_entry.GetValue()

    try:
        sql = "INSERT INTO clientes (telefono, nombre, apellido, email, direccion) VALUES (%s, %s, %s, %s, %s)"
        valores = (telefono, nombre, apellido, email, direccion)
        cursor.execute(sql, valores)
        conexion.commit()
        wx.MessageBox("Cliente creado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Error al crear cliente:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

def buscar_cliente(event):
    telefono = telefono_entry.GetValue()

    try:
        sql = "SELECT nombre, apellido, email, direccion FROM clientes WHERE telefono = %s"
        cursor.execute(sql, (telefono,))
        resultado = cursor.fetchone()
        if resultado:
            nombre_entry.SetValue(resultado[0])
            apellido_entry.SetValue(resultado[1])
            email_entry.SetValue(resultado[2])
            direccion_entry.SetValue(resultado[3])
        else:
            wx.MessageBox("Cliente no encontrado", "Aviso", wx.OK | wx.ICON_WARNING)
    except Exception as e:
        wx.MessageBox(f"Error al buscar cliente:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

def actualizar_cliente(event):
    telefono = telefono_entry.GetValue()
    nombre = nombre_entry.GetValue()
    apellido = apellido_entry.GetValue()
    email = email_entry.GetValue()
    direccion = direccion_entry.GetValue()

    try:
        sql = "UPDATE clientes SET nombre = %s, apellido = %s, email = %s, direccion = %s WHERE telefono = %s"
        valores = (nombre, apellido, email, direccion, telefono)
        cursor.execute(sql, valores)
        conexion.commit()
        wx.MessageBox("Cliente actualizado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Error al actualizar cliente:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

def eliminar_cliente(event):
    telefono = telefono_entry.GetValue()

    try:
        sql = "DELETE FROM clientes WHERE telefono = %s"
        cursor.execute(sql, (telefono,))
        conexion.commit()
        wx.MessageBox("Cliente eliminado", "Éxito", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Error al eliminar cliente:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

app = wx.App() # Crear la app
#Ventana CLIENTES
ventana2 = wx.Frame(None, title='Clientes', size=(500, 400))
panel = wx.Panel(ventana2)

# Título
titulo = wx.StaticText(panel, label="Clientes", pos=(180, 30))
fuente_titulo = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
titulo.SetFont(fuente_titulo)

# Campos del formulario
wx.StaticText(panel, label="Telefono:", pos=(50, 100))
telefono_entry = wx.TextCtrl(panel, pos=(180, 100), size=(200, -1))
telefono_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Nombre:", pos=(50, 140))
nombre_entry = wx.TextCtrl(panel, pos=(180, 140), size=(200, -1))
nombre_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Apellido:", pos=(50, 180))
apellido_entry = wx.TextCtrl(panel, pos=(180, 180), size=(200, -1))
apellido_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Email:", pos=(50, 220))
email_entry = wx.TextCtrl(panel, pos=(180, 220), size=(200, -1))
email_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Dirección:", pos=(50, 260))
direccion_entry = wx.TextCtrl(panel, pos=(180, 260), size=(200, -1))
direccion_entry.SetBackgroundColour("light gray")

#Botones
boton_ancho = 100
espaciado = 10
total_botones = 4 * boton_ancho + 3 * espaciado
inicio_x = (500 - total_botones) // 2
y_botones = 290

boton_crear = wx.Button(panel, label="Crear", pos=(inicio_x, y_botones), size=(boton_ancho, 30))
boton_buscar = wx.Button(panel, label="Buscar", pos=(inicio_x + (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
boton_actualizar = wx.Button(panel, label="Actualizar", pos=(inicio_x + 2 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
boton_eliminar = wx.Button(panel, label="Eliminar", pos=(inicio_x + 3 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))

# Conectar botones con funciones
boton_crear.Bind(wx.EVT_BUTTON, crear_cliente)
boton_buscar.Bind(wx.EVT_BUTTON, buscar_cliente)
boton_actualizar.Bind(wx.EVT_BUTTON, actualizar_cliente)
boton_eliminar.Bind(wx.EVT_BUTTON, eliminar_cliente)

ventana2.Show() #Mostrar ventana cliente
app.MainLoop()