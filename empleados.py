# Tienda Pitico - Empleados
# MARISA RIOS DE PAZ S4A

import wx
from db import conexion, cursor


class EmpleadoFrame(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title='Empleados', size=(600, 660))
        self.panel = wx.Panel(self)

        self.crear_interfaz()
        self.Centre()

    def crear_interfaz(self):
        # Título
        titulo = wx.StaticText(self.panel, label="Empleados", pos=(180, 30))
        fuente_titulo = wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        titulo.SetFont(fuente_titulo)

        # Campos del formulario
        wx.StaticText(self.panel, label="Id Empleado:", pos=(50, 100))
        self.id_empleados_entry = wx.TextCtrl(self.panel, pos=(180, 100), size=(200, -1))
        self.id_empleados_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Nombre:", pos=(50, 140))
        self.nombre_entry = wx.TextCtrl(self.panel, pos=(180, 140), size=(200, -1))
        self.nombre_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Apellido:", pos=(50, 180))
        self.apellido_entry = wx.TextCtrl(self.panel, pos=(180, 180), size=(200, -1))
        self.apellido_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Telefono:", pos=(50, 220))
        self.telefono_entry = wx.TextCtrl(self.panel, pos=(180, 220), size=(200, -1))
        self.telefono_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Email:", pos=(50, 260))
        self.email_entry = wx.TextCtrl(self.panel, pos=(180, 260), size=(200, -1))
        self.email_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Dirección:", pos=(50, 300))
        self.direccion_entry = wx.TextCtrl(self.panel, pos=(180, 300), size=(200, -1))
        self.direccion_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Puesto:", pos=(50, 340))
        self.puesto_entry = wx.TextCtrl(self.panel, pos=(180, 340), size=(200, -1))
        self.puesto_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Sueldo:", pos=(50, 380))
        self.sueldo_entry = wx.TextCtrl(self.panel, pos=(180, 380), size=(200, -1))
        self.sueldo_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Estatus:", pos=(50, 420))
        self.estatus_entry = wx.TextCtrl(self.panel, pos=(180, 420), size=(200, -1))
        self.estatus_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Contraseña:", pos=(50, 460))
        self.contrasena_entry = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD, pos=(180, 460), size=(200, -1))
        self.contrasena_entry.SetBackgroundColour("light gray")

        wx.StaticText(self.panel, label="Confirmar Contraseña:", pos=(50, 500))
        self.confirmar_contrasena_entry = wx.TextCtrl(self.panel, style=wx.TE_PASSWORD, pos=(180, 500), size=(200, -1))
        self.confirmar_contrasena_entry.SetBackgroundColour("light gray")

        # Botones
        boton_ancho = 100
        espaciado = 10
        total_botones = 4 * boton_ancho + 3 * espaciado
        inicio_x = (500 - total_botones) // 2
        y_botones = 540

        self.boton_crear = wx.Button(self.panel, label="Crear", pos=(inicio_x, y_botones), size=(boton_ancho, 30))
        self.boton_buscar = wx.Button(self.panel, label="Buscar", pos=(inicio_x + (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
        self.boton_actualizar = wx.Button(self.panel, label="Actualizar", pos=(inicio_x + 2 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))
        self.boton_eliminar = wx.Button(self.panel, label="Eliminar", pos=(inicio_x + 3 * (boton_ancho + espaciado), y_botones), size=(boton_ancho, 30))

        self.boton_ver_contrasena = wx.Button(self.panel, label="Ver Contraseña", pos=(390, 500), size=(100, 25))

        # Conectar botones con funciones
        self.boton_crear.Bind(wx.EVT_BUTTON, self.crear_empleado)
        self.boton_buscar.Bind(wx.EVT_BUTTON, self.buscar_empleado)
        self.boton_actualizar.Bind(wx.EVT_BUTTON, self.actualizar_empleado)
        self.boton_eliminar.Bind(wx.EVT_BUTTON, self.eliminar_empleado)
        self.boton_ver_contrasena.Bind(wx.EVT_BUTTON, self.ver_contrasena)

    def pedir_contrasena(self, mensaje="Ingrese su contraseña"):
        """Diálogo para ingresar contraseña"""
        dlg = wx.Dialog(self, title="Autenticación", size=(300, 150))
        sizer = wx.BoxSizer(wx.VERTICAL)

        pass_input = wx.TextCtrl(dlg, style=wx.TE_PASSWORD, size=(-1, 30))
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)

        okey = wx.Button(dlg, wx.ID_OK, "Okey")
        cancelar = wx.Button(dlg, wx.ID_CANCEL, "Cancelar")
        btn_sizer.Add(okey, 0, wx.ALL, 5)
        btn_sizer.Add(cancelar, 0, wx.ALL, 5)

        sizer.Add(wx.StaticText(dlg, label=mensaje), 0, wx.ALL, 5)
        sizer.Add(pass_input, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER)

        dlg.SetSizer(sizer)

        if dlg.ShowModal() == wx.ID_OK:
            valor = pass_input.GetValue()
            dlg.Destroy()
            return valor
        else:
            dlg.Destroy()
            return None

    def ver_contrasena(self, event):
        """Muestra la contraseña si la clave general es correcta"""
        clave_ingresada = self.pedir_contrasena("Clave General:")
        if clave_ingresada == "pitico":
            id_empleado = self.id_empleados_entry.GetValue().strip()
            if not id_empleado:
                wx.MessageBox("Por favor ingrese un ID de empleado", "Error", wx.OK | wx.ICON_ERROR)
                return

            try:
                sql = "SELECT contraseña FROM empleados WHERE id_empleado = %s"
                cursor.execute(sql, (id_empleado,))
                resultado = cursor.fetchone()
                if resultado:
                    wx.MessageBox(f"La contraseña del empleado {id_empleado} es: {resultado[0]}",
                                  "Contraseña", wx.OK | wx.ICON_INFORMATION)
                else:
                    wx.MessageBox("Empleado no encontrado", "Error", wx.OK | wx.ICON_ERROR)
            except Exception as e:
                wx.MessageBox(f"Error al obtener contraseña:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)
        elif clave_ingresada is not None:
            wx.MessageBox("Clave incorrecta", "Acceso denegado", wx.OK | wx.ICON_ERROR)

    def buscar_empleado(self, event):
        id_empleado = self.id_empleados_entry.GetValue()

        try:
            sql = """
            SELECT nombre, apellido, telefono, email, direccion, puesto, sueldo, estatus, contraseña 
            FROM empleados WHERE id_empleado = %s
            """
            cursor.execute(sql, (id_empleado,))
            resultado = cursor.fetchone()

            if resultado:
                self.nombre_entry.SetValue(resultado[0])
                self.apellido_entry.SetValue(resultado[1])
                self.telefono_entry.SetValue(resultado[2])
                self.email_entry.SetValue(resultado[3])
                self.direccion_entry.SetValue(resultado[4])
                self.puesto_entry.SetValue(resultado[5])
                self.sueldo_entry.SetValue(str(resultado[6]))
                self.estatus_entry.SetValue(resultado[7])
                self.contrasena_entry.SetValue(resultado[8])
                self.confirmar_contrasena_entry.SetValue(resultado[8])
            else:
                wx.MessageBox("Empleado no encontrado", "Aviso", wx.OK | wx.ICON_WARNING)
        except Exception as e:
            wx.MessageBox(f"Error al buscar empleado:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def actualizar_empleado(self, event):
        id_empleado = self.id_empleados_entry.GetValue()
        contrasena_actual = self.pedir_contrasena("Ingrese su contraseña actual:")
        if not contrasena_actual:
            return

        try:
            sql = "SELECT contraseña FROM empleados WHERE id_empleado = %s"
            cursor.execute(sql, (id_empleado,))
            resultado = cursor.fetchone()
            if not resultado or resultado[0] != contrasena_actual:
                wx.MessageBox("Contraseña actual incorrecta", "Error", wx.OK | wx.ICON_ERROR)
                return

            nombre = self.nombre_entry.GetValue()
            apellido = self.apellido_entry.GetValue()
            telefono = self.telefono_entry.GetValue()
            email = self.email_entry.GetValue()
            direccion = self.direccion_entry.GetValue()
            puesto = self.puesto_entry.GetValue()
            sueldo = self.sueldo_entry.GetValue()
            estatus = self.estatus_entry.GetValue()
            nueva_contrasena = self.contrasena_entry.GetValue()
            confirmar = self.confirmar_contrasena_entry.GetValue()

            if nueva_contrasena != confirmar:
                wx.MessageBox("Las contraseñas no coinciden", "Error", wx.OK | wx.ICON_ERROR)
                return

            sql = """
            UPDATE empleados 
            SET nombre = %s, apellido = %s, telefono = %s, email = %s, direccion = %s, 
                puesto = %s, sueldo = %s, estatus = %s, contraseña = %s
            WHERE id_empleado = %s
            """
            valores = (nombre, apellido, telefono, email, direccion, puesto, float(sueldo),
                       estatus, nueva_contrasena, id_empleado)
            cursor.execute(sql, valores)
            conexion.commit()
            wx.MessageBox("Empleado actualizado correctamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error al actualizar empleado:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def eliminar_empleado(self, event):
        id_empleado = self.id_empleados_entry.GetValue()
        contrasena = self.pedir_contrasena("Ingrese su contraseña actual:")
        if not contrasena:
            return

        try:
            sql = "SELECT contraseña FROM empleados WHERE id_empleado = %s"
            cursor.execute(sql, (id_empleado,))
            resultado = cursor.fetchone()

            if not resultado or resultado[0] != contrasena:
                wx.MessageBox("Contraseña incorrecta", "Error", wx.OK | wx.ICON_ERROR)
                return

            sql = "DELETE FROM empleados WHERE id_empleado = %s"
            cursor.execute(sql, (id_empleado,))
            conexion.commit()
            wx.MessageBox("Empleado eliminado", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error al eliminar empleado:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def crear_empleado(self, event):
        id_empleado = self.id_empleados_entry.GetValue()
        nombre = self.nombre_entry.GetValue()
        apellido = self.apellido_entry.GetValue()
        telefono = self.telefono_entry.GetValue()
        email = self.email_entry.GetValue()
        direccion = self.direccion_entry.GetValue()
        puesto = self.puesto_entry.GetValue()
        sueldo = self.sueldo_entry.GetValue()
        estatus = self.estatus_entry.GetValue()
        contrasena = self.contrasena_entry.GetValue()
        confirmar = self.confirmar_contrasena_entry.GetValue()

        if contrasena != confirmar:
            wx.MessageBox("Las contraseñas no coinciden", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            sql = """
            INSERT INTO empleados (id_empleado, nombre, apellido, telefono, email, direccion, puesto, sueldo, estatus, contraseña)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            valores = (id_empleado, nombre, apellido, telefono, email, direccion,
                       puesto, float(sueldo), estatus, contrasena)
            cursor.execute(sql, valores)
            conexion.commit()
            wx.MessageBox("Empleado creado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Error al crear empleado:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)