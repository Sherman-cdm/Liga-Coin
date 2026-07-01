import os
import wx
import wx.adv
from interfaz import LigaCoinApp

if __name__ == "__main__":
    app = wx.App(False)

    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ruta_splash = os.path.join(BASE_DIR, "imagenes", "Splash.png")

        img = wx.Image(ruta_splash, wx.BITMAP_TYPE_PNG)

        # Tamaño del splash 
        img = img.Scale(700, 400, wx.IMAGE_QUALITY_HIGH)

        bitmap = wx.Bitmap(img)

        splash = wx.adv.SplashScreen(
            bitmap,
            wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_TIMEOUT,
            4000,
            None,
            style=wx.BORDER_SIMPLE | wx.STAY_ON_TOP
        )
        splash.Show()

    except Exception as e:
        print(f"Error cargando splash: {e}")

    frame = LigaCoinApp()
    frame.Show()
    app.MainLoop()
