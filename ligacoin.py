# LigaCoin - Agenda Deportiva y Apuestas Virtuales
# Proyecto para la materia: Programación Orientada a Objetos
# CONCEPTOS DE POO UTILIZADOS:
#   - Clases y Objetos: Equipo, Partido, Usuario, Apuesta, LigaCoinApp
#   - Encapsulamiento: atributos privados con nombre _atributo y getters/setters
#   - Constructores (__init__) en todas las clases
#   - Métodos propios en cada clase con responsabilidades claras
#   - Asociación entre objetos: Partido contiene Equipos, Apuesta referencia
#     a Partido y Equipo, Usuario administra su lista de Apuestas

import wx
import random
import datetime


# ─────────────────────────────────────────────────────────────────────────────
# CLASE: Equipo
# ─────────────────────────────────────────────────────────────────────────────
class Equipo:
    def __init__(self, nombre):
        self._nombre = nombre

    def get_nombre(self):
        return self._nombre

    def __str__(self):
        return self._nombre


# ─────────────────────────────────────────────────────────────────────────────
# CLASE: Partido
# ─────────────────────────────────────────────────────────────────────────────
class Partido:
    PROXIMO    = "Próximo"
    EN_JUEGO   = "En juego"
    FINALIZADO = "Finalizado"

    def __init__(self, local, visitante, fecha):
        self._local           = local
        self._visitante       = visitante
        self._fecha           = fecha
        self._goles_local     = 0
        self._goles_visitante = 0
        self._estado          = Partido.PROXIMO
        self._minuto          = 0

    def get_local(self):           return self._local
    def get_visitante(self):       return self._visitante
    def get_fecha(self):           return self._fecha
    def get_goles_local(self):     return self._goles_local
    def get_goles_visitante(self): return self._goles_visitante
    def get_estado(self):          return self._estado
    def get_minuto(self):          return self._minuto

    def set_estado(self, estado):
        self._estado = estado

    def agregar_gol_local(self):
        self._goles_local += 1

    def agregar_gol_visitante(self):
        self._goles_visitante += 1

    def avanzar_minuto(self, delta=1):
        self._minuto += delta

    def get_ganador(self):
        if self._goles_local > self._goles_visitante:
            return self._local
        elif self._goles_visitante > self._goles_local:
            return self._visitante
        return None

    def get_marcador(self):
        return f"{self._goles_local} - {self._goles_visitante}"

    def __str__(self):
        return f"{self._local} vs {self._visitante}"


# ─────────────────────────────────────────────────────────────────────────────
# CLASE: Apuesta
# ─────────────────────────────────────────────────────────────────────────────
class Apuesta:
    PENDIENTE = "Pendiente"
    GANADA    = "Ganada"
    PERDIDA   = "Perdida"
    EMPATE    = "Empate"

    def __init__(self, partido, equipo_apostado, cantidad):
        self._partido         = partido
        self._equipo_apostado = equipo_apostado
        self._cantidad        = cantidad
        self._resultado       = Apuesta.PENDIENTE

    def get_partido(self):         return self._partido
    def get_equipo_apostado(self): return self._equipo_apostado
    def get_cantidad(self):        return self._cantidad
    def get_resultado(self):       return self._resultado

    def set_resultado(self, resultado):
        self._resultado = resultado

    def resolver(self):
        ganador = self._partido.get_ganador()
        if ganador is None:
            self._resultado = Apuesta.EMPATE
        elif ganador.get_nombre() == self._equipo_apostado.get_nombre():
            self._resultado = Apuesta.GANADA
        else:
            self._resultado = Apuesta.PERDIDA

    def __str__(self):
        return (f"{self._partido} | {self._equipo_apostado} | "
                f"{self._cantidad} LC | {self._resultado}")


# ─────────────────────────────────────────────────────────────────────────────
# CLASE: Usuario
# ─────────────────────────────────────────────────────────────────────────────
class Usuario:
    SALDO_INICIAL = 1000

    def __init__(self, nombre):
        self._nombre   = nombre
        self._saldo    = Usuario.SALDO_INICIAL
        self._apuestas = []

    def get_nombre(self):   return self._nombre
    def get_saldo(self):    return self._saldo
    def get_apuestas(self): return self._apuestas

    def puede_apostar(self, cantidad):
        return 0 < cantidad <= self._saldo

    def descontar(self, cantidad):
        self._saldo -= cantidad

    def acreditar(self, cantidad):
        self._saldo += cantidad

    def agregar_apuesta(self, apuesta):
        self._apuestas.append(apuesta)

    def limpiar_historial(self):
        self._apuestas.clear()

    def reiniciar(self):
        self._saldo = Usuario.SALDO_INICIAL
        self._apuestas.clear()


# ─────────────────────────────────────────────────────────────────────────────
# CLASE: VentanaBienvenida
# ─────────────────────────────────────────────────────────────────────────────
class VentanaBienvenida(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title="¡Bienvenido a LigaCoin!",
                         size=(480, 380),
                         style=wx.DEFAULT_DIALOG_STYLE | wx.STAY_ON_TOP)
        self.SetBackgroundColour(wx.Colour(245, 248, 252))
        self._construir_ui()
        self.Centre()

    def _construir_ui(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour(wx.Colour(245, 248, 252))
        sizer = wx.BoxSizer(wx.VERTICAL)

        lbl_titulo = wx.StaticText(panel, label="⚽  LigaCoin  ⚽")
        lbl_titulo.SetFont(wx.Font(22, wx.FONTFAMILY_DEFAULT,
                                   wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        lbl_titulo.SetForegroundColour(wx.Colour(30, 100, 30))

        descripcion = (
            "LigaCoin es una agenda deportiva virtual donde podés:\n\n"
            "  📅  Consultar próximos partidos de la\n"
            "        Primera División Argentina.\n\n"
            "  🔴  Ver marcadores simulados en tiempo real.\n\n"
            "  🪙  Apostar con monedas virtuales llamadas\n"
            "        LigaCoins (empezás con 1000 LC).\n\n"
            "  📊  Seguir tu historial de apuestas.\n\n"
            "¡Si acertás el ganador ganás el doble de lo apostado!"
        )
        lbl_desc = wx.StaticText(panel, label=descripcion)
        lbl_desc.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT,
                                  wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))

        btn = wx.Button(panel, label="  ¡Empezar!  ", size=(-1, 36))
        btn.SetBackgroundColour(wx.Colour(34, 139, 34))
        btn.SetForegroundColour(wx.WHITE)
        btn.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT,
                             wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        btn.Bind(wx.EVT_BUTTON, lambda e: self.EndModal(wx.ID_OK))

        sizer.AddSpacer(18)
        sizer.Add(lbl_titulo, 0, wx.ALIGN_CENTER | wx.BOTTOM, 10)
        sizer.Add(lbl_desc,   0, wx.LEFT | wx.RIGHT, 28)
        sizer.AddSpacer(16)
        sizer.Add(btn, 0, wx.ALIGN_CENTER | wx.BOTTOM, 16)

        panel.SetSizer(sizer)


# ─────────────────────────────────────────────────────────────────────────────
# CLASE: LigaCoinApp  (hereda de wx.Frame)
# ─────────────────────────────────────────────────────────────────────────────
class LigaCoinApp(wx.Frame):

    NOMBRES_EQUIPOS = [
        "Boca Juniors", "River Plate", "Racing Club", "Independiente",
        "San Lorenzo", "Vélez Sarsfield", "Estudiantes", "Gimnasia LP",
        "Rosario Central", "Newell's Old Boys", "Talleres", "Belgrano",
        "Huracán", "Lanús", "Defensa y Justicia", "Argentinos Juniors"
    ]

    def __init__(self):
        super().__init__(None,
                         title="LigaCoin - Agenda Deportiva y Apuestas Virtuales",
                         size=(900, 700),
                         style=wx.DEFAULT_FRAME_STYLE & ~wx.RESIZE_BORDER)
        self.SetBackgroundColour(wx.Colour(240, 244, 248))
        self.SetMinSize((900, 700))

        self._equipos        = [Equipo(n) for n in self.NOMBRES_EQUIPOS]
        self._usuario        = Usuario("Jugador")
        self._partidos       = []
        self._timer          = None
        self._partido_en_sim = None
        self._partido_sel    = None   # Partido actualmente seleccionado en la lista

        self._generar_partidos()
        self._construir_ui()
        self._actualizar_lista_partidos()
        self.Centre()

        dlg = VentanaBienvenida(self)
        dlg.ShowModal()
        dlg.Destroy()

    # ── Generación de partidos ────────────────────────────────────────────────
    def _generar_partidos(self):
        self._partidos.clear()
        equipos_usados = random.sample(self._equipos, len(self._equipos))
        hoy = datetime.date.today()
        for i in range(0, min(16, len(equipos_usados) - 1), 2):
            delta = random.randint(0, 14)
            fecha = hoy + datetime.timedelta(days=delta)
            partido = Partido(equipos_usados[i], equipos_usados[i + 1],
                              fecha.strftime("%d/%m/%Y"))
            self._partidos.append(partido)

    # ── Construcción de la interfaz ───────────────────────────────────────────
    def _construir_ui(self):
        panel_main = wx.Panel(self)
        panel_main.SetBackgroundColour(wx.Colour(240, 244, 248))
        sizer_main = wx.BoxSizer(wx.VERTICAL)

        # ── Encabezado ────────────────────────────────────────────────────────
        panel_header = wx.Panel(panel_main)
        panel_header.SetBackgroundColour(wx.Colour(22, 90, 22))
        sizer_header = wx.BoxSizer(wx.HORIZONTAL)

        lbl_titulo = wx.StaticText(panel_header,
            label="⚽  LigaCoin - Agenda Deportiva y Apuestas Virtuales  ⚽")
        lbl_titulo.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT,
                                   wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        lbl_titulo.SetForegroundColour(wx.WHITE)

        self._lbl_saldo = wx.StaticText(panel_header, label="🪙  1000 LC")
        self._lbl_saldo.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT,
                                        wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self._lbl_saldo.SetForegroundColour(wx.Colour(255, 230, 80))

        sizer_header.Add(lbl_titulo, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 14)
        sizer_header.Add(self._lbl_saldo, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 18)
        panel_header.SetSizer(sizer_header)
        panel_header.SetMinSize((-1, 46))

        # ── Cuerpo ────────────────────────────────────────────────────────────
        sizer_body = wx.BoxSizer(wx.HORIZONTAL)

        # Panel izquierdo
        panel_izq = wx.Panel(panel_main)
        panel_izq.SetBackgroundColour(wx.Colour(240, 244, 248))
        sizer_izq = wx.BoxSizer(wx.VERTICAL)

        lbl_partidos = wx.StaticText(panel_izq, label="📋  Partidos")
        lbl_partidos.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT,
                                      wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        lbl_partidos.SetForegroundColour(wx.Colour(22, 90, 22))

        self._lista_partidos = wx.ListCtrl(panel_izq,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN | wx.LC_SINGLE_SEL)
        self._lista_partidos.InsertColumn(0, "Local",     width=130)
        self._lista_partidos.InsertColumn(1, "Visitante", width=130)
        self._lista_partidos.InsertColumn(2, "Fecha",     width=80)
        self._lista_partidos.InsertColumn(3, "Estado",    width=80)
        self._lista_partidos.InsertColumn(4, "Marcador",  width=65)
        self._lista_partidos.Bind(wx.EVT_LIST_ITEM_SELECTED,
                                   self._on_seleccionar_partido)

        self._btn_simular = wx.Button(panel_izq, label="▶️  Iniciar Simulación",
                                       size=(-1, 34))
        self._btn_simular.SetBackgroundColour(wx.Colour(30, 120, 30))
        self._btn_simular.SetForegroundColour(wx.WHITE)
        self._btn_simular.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT,
                                           wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        self._btn_simular.Bind(wx.EVT_BUTTON, self._on_iniciar_simulacion)

        self._lbl_minuto = wx.StaticText(panel_izq, label="")
        self._lbl_minuto.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT,
                                          wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))
        self._lbl_minuto.SetForegroundColour(wx.Colour(100, 100, 100))

        btn_reiniciar = wx.Button(panel_izq, label="🔄  Reiniciar Temporada",
                                   size=(-1, 30))
        btn_reiniciar.SetBackgroundColour(wx.Colour(200, 80, 20))
        btn_reiniciar.SetForegroundColour(wx.WHITE)
        btn_reiniciar.Bind(wx.EVT_BUTTON, self._on_reiniciar_temporada)

        sizer_izq.Add(lbl_partidos,        0, wx.TOP | wx.BOTTOM, 6)
        sizer_izq.Add(self._lista_partidos,1, wx.EXPAND | wx.BOTTOM, 6)
        sizer_izq.Add(self._btn_simular,   0, wx.EXPAND | wx.BOTTOM, 4)
        sizer_izq.Add(self._lbl_minuto,    0, wx.BOTTOM, 6)
        sizer_izq.Add(btn_reiniciar,       0, wx.EXPAND | wx.BOTTOM, 6)
        panel_izq.SetSizer(sizer_izq)

        # Panel derecho
        panel_der = wx.Panel(panel_main)
        panel_der.SetBackgroundColour(wx.Colour(240, 244, 248))
        sizer_der = wx.BoxSizer(wx.VERTICAL)

        lbl_apuestas = wx.StaticText(panel_der, label="🪙  Realizar Apuesta")
        lbl_apuestas.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT,
                                      wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        lbl_apuestas.SetForegroundColour(wx.Colour(22, 90, 22))

        lbl_partido_sel = wx.StaticText(panel_der, label="Partido seleccionado:")
        self._lbl_partido_actual = wx.StaticText(panel_der,
            label="(Seleccioná un partido de la lista)")
        self._lbl_partido_actual.SetForegroundColour(wx.Colour(80, 80, 160))
        self._lbl_partido_actual.SetFont(
            wx.Font(9, wx.FONTFAMILY_DEFAULT,
                    wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))

        lbl_ganador = wx.StaticText(panel_der, label="Apostá al ganador:")
        self._choice_equipo = wx.Choice(panel_der,
                                         choices=["— Elegí un equipo —"])
        self._choice_equipo.SetSelection(0)

        lbl_cantidad = wx.StaticText(panel_der, label="Cantidad (LigaCoins):")
        self._txt_cantidad = wx.TextCtrl(panel_der, size=(160, -1))

        btn_apostar = wx.Button(panel_der, label="✅  Apostar", size=(-1, 34))
        btn_apostar.SetBackgroundColour(wx.Colour(20, 80, 180))
        btn_apostar.SetForegroundColour(wx.WHITE)
        btn_apostar.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT,
                                     wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        btn_apostar.Bind(wx.EVT_BUTTON, self._on_apostar)

        self._lbl_msg_apuesta = wx.StaticText(panel_der, label="")
        self._lbl_msg_apuesta.SetFont(
            wx.Font(9, wx.FONTFAMILY_DEFAULT,
                    wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL))

        lbl_hist = wx.StaticText(panel_der, label="📊  Historial de Apuestas")
        lbl_hist.SetFont(wx.Font(11, wx.FONTFAMILY_DEFAULT,
                                  wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        lbl_hist.SetForegroundColour(wx.Colour(22, 90, 22))

        self._lista_historial = wx.ListCtrl(panel_der,
            style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        self._lista_historial.InsertColumn(0, "Partido",   width=180)
        self._lista_historial.InsertColumn(1, "Aposté a",  width=120)
        self._lista_historial.InsertColumn(2, "Cantidad",  width=70)
        self._lista_historial.InsertColumn(3, "Resultado", width=75)

        btn_limpiar = wx.Button(panel_der, label="🗑  Limpiar Historial",
                                 size=(-1, 30))
        btn_limpiar.SetBackgroundColour(wx.Colour(140, 30, 30))
        btn_limpiar.SetForegroundColour(wx.WHITE)
        btn_limpiar.Bind(wx.EVT_BUTTON, self._on_limpiar_historial)

        sizer_der.Add(lbl_apuestas,             0, wx.TOP | wx.BOTTOM, 6)
        sizer_der.Add(lbl_partido_sel,          0, wx.BOTTOM, 2)
        sizer_der.Add(self._lbl_partido_actual, 0, wx.BOTTOM, 8)
        sizer_der.Add(lbl_ganador,              0, wx.BOTTOM, 2)
        sizer_der.Add(self._choice_equipo,      0, wx.EXPAND | wx.BOTTOM, 8)
        sizer_der.Add(lbl_cantidad,             0, wx.BOTTOM, 2)
        sizer_der.Add(self._txt_cantidad,       0, wx.EXPAND | wx.BOTTOM, 8)
        sizer_der.Add(btn_apostar,              0, wx.EXPAND | wx.BOTTOM, 4)
        sizer_der.Add(self._lbl_msg_apuesta,    0, wx.BOTTOM, 8)
        sizer_der.Add(wx.StaticLine(panel_der), 0, wx.EXPAND | wx.BOTTOM, 6)
        sizer_der.Add(lbl_hist,                 0, wx.BOTTOM, 4)
        sizer_der.Add(self._lista_historial,    1, wx.EXPAND | wx.BOTTOM, 6)
        sizer_der.Add(btn_limpiar,              0, wx.EXPAND | wx.BOTTOM, 6)
        panel_der.SetSizer(sizer_der)

        sizer_body.Add(panel_izq, 3, wx.EXPAND | wx.LEFT | wx.RIGHT, 10)
        sizer_body.Add(panel_der, 2, wx.EXPAND | wx.RIGHT, 10)

        # ── Pie de página ─────────────────────────────────────────────────────
        panel_footer = wx.Panel(panel_main)
        panel_footer.SetBackgroundColour(wx.Colour(210, 220, 210))
        sizer_footer = wx.BoxSizer(wx.HORIZONTAL)
        lbl_footer = wx.StaticText(panel_footer,
            label="Proyecto realizado para Programación Orientada a Objetos  —  "
                  "Clases: Equipo · Partido · Usuario · Apuesta · LigaCoinApp")
        lbl_footer.SetFont(wx.Font(8, wx.FONTFAMILY_DEFAULT,
                                   wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL))
        lbl_footer.SetForegroundColour(wx.Colour(80, 80, 80))
        sizer_footer.Add(lbl_footer, 1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        panel_footer.SetSizer(sizer_footer)
        panel_footer.SetMinSize((-1, 28))

        sizer_main.Add(panel_header, 0, wx.EXPAND)
        sizer_main.Add(sizer_body,   1, wx.EXPAND | wx.TOP | wx.BOTTOM, 8)
        sizer_main.Add(panel_footer, 0, wx.EXPAND)
        panel_main.SetSizer(sizer_main)

    # ── Actualizar lista de partidos ──────────────────────────────────────────
    def _actualizar_lista_partidos(self):
        self._lista_partidos.DeleteAllItems()
        for p in self._partidos:
            idx = self._lista_partidos.InsertItem(
                self._lista_partidos.GetItemCount(),
                p.get_local().get_nombre())
            self._lista_partidos.SetItem(idx, 1, p.get_visitante().get_nombre())
            self._lista_partidos.SetItem(idx, 2, p.get_fecha())
            self._lista_partidos.SetItem(idx, 3, p.get_estado())
            self._lista_partidos.SetItem(idx, 4, p.get_marcador())

    # ── Actualizar label de saldo ─────────────────────────────────────────────
    def _actualizar_saldo(self):
        self._lbl_saldo.SetLabel(f"🪙  {self._usuario.get_saldo()} LC")

    # ── Eventos ───────────────────────────────────────────────────────────────
    def _on_seleccionar_partido(self, event):
        idx = event.GetIndex()
        self._partido_sel = self._partidos[idx]
        p = self._partido_sel
        self._lbl_partido_actual.SetLabel(str(p))

        # Cargar los dos equipos en el choice
        self._choice_equipo.Clear()
        self._choice_equipo.Append(p.get_local().get_nombre())
        self._choice_equipo.Append(p.get_visitante().get_nombre())
        self._choice_equipo.SetSelection(0)
        self._lbl_msg_apuesta.SetLabel("")

    def _on_apostar(self, event):
        self._lbl_msg_apuesta.SetLabel("")

        if self._partido_sel is None:
            self._lbl_msg_apuesta.SetForegroundColour(wx.Colour(180, 0, 0))
            self._lbl_msg_apuesta.SetLabel("⚠ Seleccioná un partido primero.")
            return

        if self._partido_sel.get_estado() == Partido.FINALIZADO:
            self._lbl_msg_apuesta.SetForegroundColour(wx.Colour(180, 0, 0))
            self._lbl_msg_apuesta.SetLabel("⚠ Ese partido ya finalizó.")
            return

        # Validar cantidad
        try:
            cantidad = int(self._txt_cantidad.GetValue())
        except ValueError:
            self._lbl_msg_apuesta.SetForegroundColour(wx.Colour(180, 0, 0))
            self._lbl_msg_apuesta.SetLabel("⚠ Ingresá una cantidad válida.")
            return

        if not self._usuario.puede_apostar(cantidad):
            self._lbl_msg_apuesta.SetForegroundColour(wx.Colour(180, 0, 0))
            self._lbl_msg_apuesta.SetLabel("⚠ Saldo insuficiente o cantidad inválida.")
            return

        # Obtener equipo elegido
        sel = self._choice_equipo.GetSelection()
        if sel == wx.NOT_FOUND:
            self._lbl_msg_apuesta.SetForegroundColour(wx.Colour(180, 0, 0))
            self._lbl_msg_apuesta.SetLabel("⚠ Elegí un equipo.")
            return

        nombre_eq = self._choice_equipo.GetString(sel)
        if nombre_eq == self._partido_sel.get_local().get_nombre():
            equipo_apostado = self._partido_sel.get_local()
        else:
            equipo_apostado = self._partido_sel.get_visitante()

        # Crear y registrar apuesta
        apuesta = Apuesta(self._partido_sel, equipo_apostado, cantidad)
        self._usuario.descontar(cantidad)
        self._usuario.agregar_apuesta(apuesta)
        self._actualizar_saldo()
        self._actualizar_historial()

        self._lbl_msg_apuesta.SetForegroundColour(wx.Colour(0, 120, 0))
        self._lbl_msg_apuesta.SetLabel(
            f"✅ Apostaste {cantidad} LC a {equipo_apostado}.")
        self._txt_cantidad.SetValue("")

    def _on_iniciar_simulacion(self, event):
        if self._partido_sel is None:
            wx.MessageBox("Seleccioná un partido para simular.",
                          "Aviso", wx.OK | wx.ICON_INFORMATION)
            return

        if self._partido_sel.get_estado() == Partido.FINALIZADO:
            wx.MessageBox("Ese partido ya finalizó.", "Aviso",
                          wx.OK | wx.ICON_INFORMATION)
            return

        if self._timer is not None and self._timer.IsRunning():
            wx.MessageBox("Ya hay una simulación en curso.", "Aviso",
                          wx.OK | wx.ICON_INFORMATION)
            return

        self._partido_en_sim = self._partido_sel
        self._partido_en_sim.set_estado(Partido.EN_JUEGO)
        self._btn_simular.Disable()
        self._lbl_minuto.SetLabel("⏱ Minuto 0'")

        self._timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._on_tick_simulacion, self._timer)
        self._timer.Start(200)   # Cada 200 ms = 1 minuto simulado

    def _on_tick_simulacion(self, event):
        p = self._partido_en_sim
        p.avanzar_minuto()
        minuto = p.get_minuto()

        # Probabilidad de gol: ~3 goles por partido en promedio
        if random.random() < 0.025:
            if random.random() < 0.5:
                p.agregar_gol_local()
            else:
                p.agregar_gol_visitante()

        self._lbl_minuto.SetLabel(f"⏱ Minuto {minuto}'  |  {p.get_marcador()}")
        self._actualizar_lista_partidos()

        if minuto >= 90:
            self._timer.Stop()
            p.set_estado(Partido.FINALIZADO)
            self._actualizar_lista_partidos()
            self._lbl_minuto.SetLabel(
                f"✅ Partido finalizado  |  {p.get_marcador()}")
            self._btn_simular.Enable()
            self._resolver_apuestas_del_partido(p)

    def _resolver_apuestas_del_partido(self, partido):
        resueltas = 0
        ganancia_total = 0
        for apuesta in self._usuario.get_apuestas():
            if (apuesta.get_partido() is partido
                    and apuesta.get_resultado() == Apuesta.PENDIENTE):
                apuesta.resolver()
                if apuesta.get_resultado() == Apuesta.GANADA:
                    premio = apuesta.get_cantidad() * 2
                    self._usuario.acreditar(premio)
                    ganancia_total += premio
                resueltas += 1

        self._actualizar_saldo()
        self._actualizar_historial()

        if resueltas > 0:
            ganador = partido.get_ganador()
            msg = (f"Partido finalizado: {partido.get_marcador()}\n"
                   f"Ganador: {ganador if ganador else 'Empate'}\n")
            if ganancia_total > 0:
                msg += f"🎉 ¡Ganaste! Se acreditaron {ganancia_total} LC."
            else:
                msg += "😞 No ganaste esta vez."
            wx.MessageBox(msg, "Resultado", wx.OK | wx.ICON_INFORMATION)

    def _actualizar_historial(self):
        self._lista_historial.DeleteAllItems()
        for a in self._usuario.get_apuestas():
            idx = self._lista_historial.InsertItem(
                self._lista_historial.GetItemCount(),
                str(a.get_partido()))
            self._lista_historial.SetItem(idx, 1,
                                           a.get_equipo_apostado().get_nombre())
            self._lista_historial.SetItem(idx, 2, str(a.get_cantidad()))
            self._lista_historial.SetItem(idx, 3, a.get_resultado())

    def _on_limpiar_historial(self, event):
        self._usuario.limpiar_historial()
        self._actualizar_historial()

    def _on_reiniciar_temporada(self, event):
        if self._timer is not None and self._timer.IsRunning():
            self._timer.Stop()
        self._usuario.reiniciar()
        self._generar_partidos()
        self._partido_sel    = None
        self._partido_en_sim = None
        self._btn_simular.Enable()
        self._lbl_minuto.SetLabel("")
        self._lbl_partido_actual.SetLabel("(Seleccioná un partido de la lista)")
        self._choice_equipo.Clear()
        self._choice_equipo.Append("— Elegí un equipo —")
        self._choice_equipo.SetSelection(0)
        self._lbl_msg_apuesta.SetLabel("")
        self._actualizar_saldo()
        self._actualizar_lista_partidos()
        self._actualizar_historial()


# ─────────────────────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = wx.App(False)
    frame = LigaCoinApp()
    frame.Show()
    app.MainLoop()
