# Liga-Coin
Segui en tiempo real partidos/resultados/estadisticas y juga tu suerte apostando Coins
LigaCión es una aplicación de escritorio desarrollada en Python con la biblioteca gráfica wxPython. Simula una agenda deportiva donde el usuario puede consultar partidos de la Primera División Argentina, ver marcadores en tiempo real (simulados por un temporizador interno) y realizar apuestas con una moneda virtual llamada LigaCión (LC). Al abrir la aplicación aparece una ventana de bienvenida que explica las funcionalidades disponibles y le da al usuario la posibilidad de empezar. El jugador parte con un saldo inicial de 1.000 LC y puede apostar a distintos partidos antes o durante su simulación 

<img width="417" height="331" alt="image" src="https://github.com/user-attachments/assets/31d27750-f942-4ac4-b262-5fab75363d19" />

# CONCEPTOS DE POO UTILIZADOS:
#   - Clases y Objetos: Equipo, Partido, Usuario, Apuesta, LigaCoinApp
#   - Encapsulamiento: atributos privados con nombre _atributo y getters/setters
#   - Constructores (__init__) en todas las clases
#   - Métodos propios en cada clase con responsabilidades claras
#   - Asociación entre objetos: Partido contiene Equipos, Apuesta referencia
#     a Partido y Equipo, Usuario administra su lista de Apuestas
