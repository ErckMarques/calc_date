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
from PIL import Image
from tkinter import Event
from PIL import Image, ImageTk
from ttkbootstrap import Window, PhotoImage
from ttkbootstrap.tooltip import ToolTip

from date_calc.gui import find_image, ICON_PATH
from date_calc.gui.frame_date_difference import FrameDateDifference
from date_calc.gui.frame_data_interval import FrameDateWithInterval
from date_calc.gui.utils.grid_layout import ConfigureGridLayout

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
        # Add widgets
        self._add_widgets()

    def _configuration_of_window(self) -> None:
        """
        Configures window and class-level bindings (bind_class)
        """
        self.title("Day Counter and Date Calculator")
        self.resizable(False, False)
        self.bind("<Escape>", lambda e: self.focus_set())
        # Configure grid layout for widgets
        self.configure_grid_layout(self, rows=3, columns=1)
        if sys.platform == "win32":
            self.iconbitmap(find_image("date_calc"))
        else:
            # Linux and macOS
            self.iconphoto(True, find_image("date_calc"))

    def _minimize_to_tray(self) -> None:
        """
        Minimize the window to system tray.
        """
        self.withdraw()  # Hide the window
        
        # Create tray icon if it doesn't exist
        if not hasattr(self, '_tray_icon') or self._tray_icon is None:
            self._create_tray_icon()
        else:
            # If icon exists but was stopped, recreate it
            self._tray_icon.stop()
            self._create_tray_icon()

    def _create_tray_icon(self) -> None:
        """
        Create the system tray icon.
        """
        try:
            # Load icon image
            image = Image.open(find_image("date_calc"))
        except FileNotFoundError:
            # Fallback: create a simple image if file not found
            image = Image.new('RGB', (64, 64), color='blue')
        
        # Create tray menu
        menu = pystray.Menu(
            pystray.MenuItem("Show", self._restore_from_tray),
            pystray.MenuItem("Exit", self._quit_application)
        )
        
        # Create and run tray icon (non-blocking)
        self._tray_icon = pystray.Icon(
            "date_calculator", 
            image, 
            "Date Calculator", 
            menu
        )
        self._tray_icon.run_detached()

    def _restore_from_tray(self) -> None:
        """
        Restore the window from system tray.
        """
        if hasattr(self, '_tray_icon') and self._tray_icon:
            self._tray_icon.stop()
            self._tray_icon = None
        
        # Restore the window
        self.deiconify()
        self.lift()
        self.focus_force()

    def _quit_application(self) -> None:
        """
        Quit the application completely.
        """
        if hasattr(self, '_tray_icon') and self._tray_icon:
            self._tray_icon.stop()
        self.destroy()

    def _add_widgets(self) -> None:
        """
        Add widgets to the main window.
        """
        FrameDateDifference(self).pack(pady=10, padx=10, fill="both", expand=True)
        self._add_frame_buttons()
        FrameDateWithInterval(self).pack(pady=10, padx=10, fill="both", expand=True)

    def _add_frame_buttons(self) -> None:
        frame = ttk.Frame(self)
<<<<<<< HEAD
        frame.pack(pady=10, padx=10, fill="both", expand=True, side='bottom') # The bottom frame for buttons always placed at the end of the screen
        
        # Configuration button
        image = PhotoImage(name="config_icon", file=ICON_PATH.parent.joinpath("png", "config.png"))
        ttk.Button(frame, text="Configuration", image=image, compound="center", command=self._top_config).pack(side="left", padx=5)
        
        # Tray System button - now functional
        ttk.Button(
            frame, 
            text="Tray System", 
            command=self._minimize_to_tray  # Changed to use the tray function
        ).pack(side="left", padx=5)
=======
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
>>>>>>> 9289e2274c6119a2422f8b0b27e257d3f6c1afb7

    def _development(self):
        """open the development window"""
        top = ttk.Toplevel(title="Development")
        # Add development widgets here
        top.iconbitmap(find_image("develop"))
        ttk.Label(top, text="Development Window in development").pack(pady=20)

    def _top_config(self):
        """open the top configuration window"""
        top = ttk.Toplevel(title="Configuration")
        # Add configuration widgets here
        top.iconbitmap(find_image("config"))
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
        app = TWindow(themename="darkly")
        app.mainloop()
    except KeyboardInterrupt as e:
        print("Encerrando a aplicação")
        exit(0) #? Aqui o código deve ser encerrado corretamente