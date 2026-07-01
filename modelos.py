# =============================================================================
# MODELOS (modelos.py)
# =============================================================================
import random

class Equipo:
    def __init__(self, nombre):
        self._nombre = nombre

    def get_nombre(self):
        return self._nombre

    def __str__(self):
        return self._nombre


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
    
        elif ganador == self._equipo_apostado: 
            self._resultado = Apuesta.GANADA
        else:
            self._resultado = Apuesta.PERDIDA

    def __str__(self):
        return (f"{self._partido} | {self._equipo_apostado} | "
                f"{self._cantidad} LC | {self._resultado}")


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