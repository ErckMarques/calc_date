"""
This file provides a TWindow class, which inherits from ttkbootstrap.Window, marked with the typing.final decorator.
This TWindow holds all the logic related to the application's main window.
"""
from textwrap import dedent
from typing import final
from pathlib import Path

import sys
import pystray
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from ttkbootstrap import Window, PhotoImage
from ttkbootstrap.tooltip import ToolTip

from date_calc.gui.frame_date_difference import ConfigureGridLayout, FrameDateDifference
from date_calc.gui.frame_data_interval import FrameDateWithInterval

from date_calc import ICON_PATH


@final
class TWindow(Window, ConfigureGridLayout):
    """
    TWindow class that extends ttkbootstrap.Window.
    This class is intended to hold all the logic related to the application's main window.
    It receives the same arguments as the parent class.
    """

    def __init__(
            self,
            title="ttkbootstrap",
            themename="litera",
            iconphoto='',
            size=None,
            position=None,
            minsize=None,
            maxsize=None,
            resizable=None,
            hdpi=True,
            scaling=None,
            transient=None,
            overrideredirect=False,
            alpha=1.0,
            **kwargs,
        ) -> None:
        super().__init__(
            title=title,
            themename=themename,
            iconphoto=iconphoto,
            size=size,
            position=position,
            minsize=minsize,
            maxsize=maxsize,
            resizable=resizable,
            hdpi=hdpi,
            scaling=scaling,
            transient=transient,
            overrideredirect=overrideredirect,
            alpha=alpha,
            **kwargs,
        )

        # configuration
        self._configuration_of_window()
        # Add behavior to the system tray icon.
        # self._configure_py_stray()
        # Add widgets
        self._add_widgets()

    def _configuration_of_window(self) -> None:
        """
        Configure the window settings.
        """
        self.resizable(False, False)
        
        self.bind("<Escape>", lambda e: self.focus_set())
        # Configure grid layout for widgets
        self.configure_grid_layout(self, rows=3, columns=1)
        if sys.platform == "win32":
            self.iconbitmap(ICON_PATH.joinpath("date_calc.ico"))
        else:
            # Linux and macOS
            self.iconphoto(True, PhotoImage(file=ICON_PATH.joinpath("date_calc.png")))


    def _configure_py_stray(self) -> None:
        """
        Add behavior to the system tray icon.
        """
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _on_close(self) -> None:
        """
        Handle the window close event.
        """
        self.withdraw()
        image = Image.open(ICON_PATH)
        menu = (
            pystray.MenuItem("Show", self._on_show),
            pystray.MenuItem("Exit", self._on_exit)
        )
        self.icon = pystray.Icon("Date Calculator", image, "Date Calculator", menu)
        self.icon.run()
        self.ico = image

    def _on_show(self) -> None:
        """
        Show the main window when the system tray icon is clicked.
        """
        self.icon.stop()
        self.after(0, self.deiconify)
    
    def _on_exit(self) -> None:
        """
        Exit the application when the system tray icon is clicked.
        """
        self.icon.stop()
        self.destroy()

    def _add_widgets(self) -> None:
        """
        Add widgets to the main window.
        """
        FrameDateDifference(self).pack(pady=10, padx=10, fill="both", expand=True)
        FrameDateWithInterval(self).pack(pady=10, padx=10, fill="both", expand=True)
        self._add_frame_buttons()

    def _add_frame_buttons(self) -> None:
        frame = ttk.Frame(self)
        # self.configure_grid_layout(frame, rows=1, columns=2)
        frame.pack(pady=10, padx=10, fill="both", expand=True)

        image = PhotoImage(name="config_icon", file=ICON_PATH.joinpath('config.png')).subsample(30)
        btn_config = ttk.Button(frame, image=image, command=self._top_config,)
        setattr(btn_config, "_image", image)  # keep a reference!
        btn_config.pack(side="left", padx=5)
        ToolTip(btn_config, "Open configuration window", bootstyle="info")

        image_tray = PhotoImage(name="tray_icon", file=ICON_PATH.joinpath('ocultar.png')).subsample(30)
        btn_tray = ttk.Button(frame, image=image_tray, command=self._development)
        setattr(btn_tray, "_image", image_tray)  # keep a reference!
        btn_tray.pack(side="left", padx=5)
        ToolTip(btn_tray, "Minimize to tray", bootstyle="info")

    def _development(self):
        """open the development window"""
        top = ttk.Toplevel(title="Development")
        # Add development widgets here
        top.iconbitmap(ICON_PATH.joinpath("develop.ico"))
        ttk.Label(top, text="Development Window in development").pack(pady=20)

    def _top_config(self):
        """open the top configuration window"""
        top = ttk.Toplevel(title="Configuration")
        # Add configuration widgets here
        top.iconbitmap(ICON_PATH.joinpath("config.ico"))
        top.title("Configuration")
        top.geometry("400x300")
        ttk.Label(top, text="Configuration Window in development").pack(pady=20)
        ttk.Label(
            top, 
            text=dedent(
                """
                This button opens the application's configuration page. It should be an inherited TopLevel, specialized in configuration issues.
                    Some configuration options:
                    - Language and localization (pt-br and english) [internationalization]
                    - Light and dark theme change
                    - Holiday calendar configuration:
                        In the backend, use a specialized class to receive a JSON or CSV file of holidays, convert it, and save it as structured JSON.
                        Also, extend the functionality of the datetime library with a simple holiday check function, "is_holiday() -> bool". 
                        Receive more than one holiday calendar and select them from a list box (if possible).
            """,)
        ).pack(pady=5)
        top.transient(self)

if __name__ == "__main__":
    # Example usage of TWindow
    try:       
        app = TWindow(title="Date Calculator", themename="darkly")
        app.mainloop()
    except KeyboardInterrupt as e:
        print("Encerrando a aplicação")
        exit(0) #? Aqui o código deve ser encerrado corretamente
