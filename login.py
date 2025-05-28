# login.py
import wx
from menu import MenuPrincipal

class LoginFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Login - Tienda Pitico", size=(600, 400))
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(202, 225, 255))
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Título
        title = wx.StaticText(panel, label="Inicio de Sesión")
        title.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        sizer.Add(title, 0, wx.ALIGN_CENTER | wx.ALL, 20)

        # Campo usuario
        self.user = wx.TextCtrl(panel)
        sizer.Add(wx.StaticText(panel, label="Usuario:"), 0, wx.LEFT, 10)
        sizer.Add(self.user, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)

        # Campo contraseña
        self.passw = wx.TextCtrl(panel, style=wx.TE_PASSWORD)
        sizer.Add(wx.StaticText(panel, label="Contraseña:"), 0, wx.LEFT, 10)
        sizer.Add(self.passw, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)

        # Botón iniciar
        btn_login = wx.Button(panel, label="Iniciar Sesión")
        btn_login.Bind(wx.EVT_BUTTON, self.on_login)
        sizer.Add(btn_login, 0, wx.ALIGN_CENTER | wx.TOP, 20)

        panel.SetSizer(sizer)
        self.Centre()
        self.Show()

    def on_login(self, event):
        from db import conexion, cursor  # Importamos conexión a BD

        usuario = self.user.GetValue().strip()
        contrasena = self.passw.GetValue().strip()

        if not usuario or not contrasena:
            wx.MessageBox("Por favor ingrese ambos campos", "Campos vacíos", wx.OK | wx.ICON_WARNING)
            return

        try:
            sql = "SELECT contraseña FROM empleados WHERE id_empleado = %s"
            cursor.execute(sql, (usuario,))
            resultado = cursor.fetchone()

            if resultado and resultado[0] == contrasena:
                # Obtener nombre del empleado para pasarlo al menú
                try:
                    sql_nombre = "SELECT nombre FROM empleados WHERE id_empleado = %s"
                    cursor.execute(sql_nombre, (usuario,))
                    nombre_resultado = cursor.fetchone()
                    nombre_empleado = nombre_resultado[0] if nombre_resultado else "Empleado"
                except Exception as e:
                    wx.MessageBox(f"Error al obtener nombre del empleado:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)
                    nombre_empleado = "Empleado"

                self.Close()
                frame = MenuPrincipal(nombre_usuario=nombre_empleado)
                frame.Show()
            else:
                wx.MessageBox("Usuario o contraseña incorrectos", "Error", wx.OK | wx.ICON_ERROR)
        except Exception as e:
            wx.MessageBox(f"Error al validar credenciales:\n{str(e)}", "Error", wx.OK | wx.ICON_ERROR)

