#Tienda Pitico 
#MARISA RIOS DE PAZ S4A

import wx
from db import conexion, cursor

def crear_empleado(event):
    id_empleado = id_empleados_entry.GetValue()
    nombre = nombre_entry.GetValue()
    apellido = apellido_entry.GetValue()
    telefono = telefono_entry.GetValue()
    email = email_entry.GetValue()
    direccion = direccion_entry.GetValue()
    puesto = puesto_entry.GetValue()
    sueldo = sueldo_entry.GetValue()
    estatus = estatus_entry.GetValue()

    try:
        sql = """
        INSERT INTO empleados (id_empleado, nombre, apellido, telefono, email, direccion, puesto, sueldo, estatus)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (id_empleado, nombre, apellido, telefono, email, direccion, puesto, sueldo, estatus)
        cursor.execute(sql, valores)
        conexion.commit()
        wx.MessageBox("Empleado creado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Error al crear empleado:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

def buscar_empleado(event):
    id_empleado = id_empleados_entry.GetValue()

    try:
        sql = "SELECT nombre, apellido, telefono, email, direccion, puesto, sueldo, estatus FROM empleados WHERE id_empleado = %s"
        cursor.execute(sql, (id_empleado,))
        resultado = cursor.fetchone()
        if resultado:
            nombre_entry.SetValue(resultado[0])
            apellido_entry.SetValue(resultado[1])
            telefono_entry.SetValue(resultado[2])
            email_entry.SetValue(resultado[3])
            direccion_entry.SetValue(resultado[4])
            puesto_entry.SetValue(resultado[5])
            sueldo_entry.SetValue(str(resultado[6]))
            estatus_entry.SetValue(resultado[7])
        else:
            wx.MessageBox("Empleado no encontrado", "Aviso", wx.OK | wx.ICON_WARNING)
    except Exception as e:
        wx.MessageBox(f"Error al buscar empleado:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

def actualizar_empleado(event):
    id_empleado = id_empleados_entry.GetValue()
    nombre = nombre_entry.GetValue()
    apellido = apellido_entry.GetValue()
    telefono = telefono_entry.GetValue()
    email = email_entry.GetValue()
    direccion = direccion_entry.GetValue()
    puesto = puesto_entry.GetValue()
    sueldo = sueldo_entry.GetValue()
    estatus = estatus_entry.GetValue()

    try:
        sql = """
        UPDATE empleados 
        SET nombre = %s, apellido = %s, telefono = %s, email = %s, direccion = %s, 
            puesto = %s, sueldo = %s, estatus = %s
        WHERE id_empleado = %s
        """
        valores = (nombre, apellido, telefono, email, direccion, puesto, sueldo, estatus, id_empleado)
        cursor.execute(sql, valores)
        conexion.commit()
        wx.MessageBox("Empleado actualizado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Error al actualizar empleado:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

def eliminar_empleado(event):
    id_empleado = id_empleados_entry.GetValue()

    try:
        sql = "DELETE FROM empleados WHERE id_empleado = %s"
        cursor.execute(sql, (id_empleado,))
        conexion.commit()
        wx.MessageBox("Empleado eliminado", "Éxito", wx.OK | wx.ICON_INFORMATION)
    except Exception as e:
        wx.MessageBox(f"Error al eliminar empleado:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

app = wx.App() #crear la app

#Ventana EMPLEADOS
ventana3 = wx.Frame(None, title='Empleados', size=(500, 550))
panel = wx.Panel(ventana3)

titulo = wx.StaticText(panel, label="Empleados", pos=(180, 30))
fuente_titulo = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
titulo.SetFont(fuente_titulo)

# Campos del formulario
wx.StaticText(panel, label="Id Empleado:", pos=(50, 100))
id_empleados_entry = wx.TextCtrl(panel, pos=(180, 100), size=(200, -1))
id_empleados_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Nombre:", pos=(50, 140))
nombre_entry = wx.TextCtrl(panel, pos=(180, 140), size=(200, -1))
nombre_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Apellido:", pos=(50, 180))
apellido_entry = wx.TextCtrl(panel, pos=(180, 180), size=(200, -1))
apellido_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Telefono:", pos=(50, 220))
telefono_entry = wx.TextCtrl(panel, pos=(180, 220), size=(200, -1))
telefono_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Email:", pos=(50, 260))
email_entry = wx.TextCtrl(panel, pos=(180, 260), size=(200, -1))
email_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Dirección:", pos=(50, 300))
direccion_entry = wx.TextCtrl(panel, pos=(180, 300), size=(200, -1))
direccion_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Puesto:", pos=(50, 340))
puesto_entry = wx.TextCtrl(panel, pos=(180, 340), size=(200, -1))
puesto_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Sueldo:", pos=(50, 380))
sueldo_entry = wx.TextCtrl(panel, pos=(180, 380), size=(200, -1))
sueldo_entry.SetBackgroundColour("light gray")

wx.StaticText(panel, label="Estatus:", pos=(50, 420))
estatus_entry = wx.TextCtrl(panel, pos=(180, 420), size=(200, -1))
estatus_entry.SetBackgroundColour("light gray")

#Botones
boton_ancho = 100
espaciado = 10
total_botones = 4 * boton_ancho + 3 * espaciado
inicio_x = (500 - total_botones) // 2
y_botones = 470

boton_crear = wx.Button(panel, label="Crear", pos=(inicio_x, y_botones), size=(boton_ancho, 30))
boton_buscar = wx.Button(panel, label="Buscar", pos=(inicio_x + (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
boton_actualizar = wx.Button(panel, label="Actualizar", pos=(inicio_x + 2 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
boton_eliminar = wx.Button(panel, label="Eliminar", pos=(inicio_x + 3 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))

boton_crear.Bind(wx.EVT_BUTTON, crear_empleado)
boton_buscar.Bind(wx.EVT_BUTTON, buscar_empleado)
boton_actualizar.Bind(wx.EVT_BUTTON, actualizar_empleado)
boton_eliminar.Bind(wx.EVT_BUTTON, eliminar_empleado)

ventana3.Show()
app.MainLoop()