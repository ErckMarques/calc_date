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
from ttkbootstrap import Window, PhotoImage
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.dialogs import Messagebox

from date_calc.gui.frame_date_difference import FrameDateDifference
from date_calc.gui.frame_data_interval import FrameDateWithInterval
from date_calc.gui.utils.grid_layout import ConfigureGridLayout

from date_calc import ICON_PATH, t


@final
class TWindow(Window, ConfigureGridLayout):
    """
    TWindow class that extends ttkbootstrap.Window.
    This class is intended to hold all the logic related to the application's main window.
    It receives the same arguments as the parent class.
    """

    def __init__(
            self,
            **kwargs,
        ) -> None:
        super().__init__(**kwargs)

        # configuration
        self._configuration_of_window()
        # Add widgets
        self._add_widgets()

    def _configuration_of_window(self) -> None:
        """
        Configures window and class-level bindings (bind_class)
        """
        self.title(t['main']["app_title"])
        self.resizable(False, False)
        self.bind("<Escape>", lambda e: self.focus_set())
        
        # Configure grid layout for widgets
        self.configure_grid_layout(self, rows=3, columns=1)
        
        if sys.platform == "win32":
            self.iconbitmap(ICON_PATH.joinpath("date_calc.ico"), default=ICON_PATH.joinpath("date_calc.ico").as_posix())
        else:
            # Linux and macOS
            self.iconphoto(True, ICON_PATH.joinpath("date_calc.png"))

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
            # self._create_tray_icon()

    def _create_tray_icon(self) -> None:
        """
        Create the system tray icon.
        """
        try:
            # Load icon image
            image = Image.open(ICON_PATH.joinpath("date_calc.ico"))
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
            t['main']["tray_icon_tooltip"], 
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
        # fix this
        if hasattr(self, '_tray_icon') and self._tray_icon:
            self._tray_icon.stop()
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
        self.configure_grid_layout(frame, rows=1, columns=2)
        frame.pack(pady=10, padx=10, anchor="sw", expand=True, side="left")

        image = PhotoImage(name="config_icon", file=ICON_PATH.joinpath('config.png')).subsample(30)
        btn_config = ttk.Button(frame, image=image, command=self._development,)
        setattr(btn_config, "_image", image)  # keep a reference!
        btn_config.pack(side="left", padx=5)
        ToolTip(btn_config, t['main']['btn_config_tooltip'], bootstyle="info")

        image_tray = PhotoImage(name="tray_icon", file=ICON_PATH.joinpath('ocultar.png')).subsample(30)
        btn_tray = ttk.Button(frame, image=image_tray, command=self._minimize_to_tray)
        setattr(btn_tray, "_image", image_tray)  # keep a reference!
        btn_tray.pack(side="left", padx=5)
        ToolTip(btn_tray, t['main']['btn_tray_tooltip'], bootstyle="info")

        # switcher theme
        on_img = PhotoImage(name="on_icon", file=ICON_PATH.joinpath('light.png')).subsample(30)
        swtch_btn = ttk.Button(frame, image=on_img, command=lambda :self._switch_theme(swtch_btn))
        swtch_btn.pack(side='left', padx=5)
        setattr(swtch_btn, "_image", on_img)
        ToolTip(swtch_btn, text=t['main']['btn_switch_tooltip'], bootstyle="info")

    def _switch_theme(self, button: ttk.Button):
        """Switch the application theme."""
        if self.style.theme_use() == "darkly":
            self.style.theme_use("litera")
            # off_img = PhotoImage(name="off_icon", file=ICON_PATH.joinpath('dark.png')).subsample(30)
            # setattr(button, "_image", off_img)
        else:
            self.style.theme_use("darkly")
            # on_img = PhotoImage(name="on_icon", file=ICON_PATH.joinpath('light.png')).subsample(30)
            # setattr(button, "_image", on_img)

    def _development(self):
        """open the development window"""
        Messagebox.show_info(
            message=dedent(
            """
            Em desenvolvimento
            """
            ),
            title="resource under development".title(),
            parent=self,
        )

    def _top_config(self):
        """open the top configuration window"""
        Messagebox.show_info(
            title="configuration menu under development".capitalize(),
            message=dedent(
                """
                This button opens the application's configuration page. It should be an inherited TopLevel, specialized in configuration issues.
                    Some configuration options:
                    - Language and localization (pt-br and english) [internationalization]
                    - Light and dark theme change
                    - Holiday calendar configuration:
                        In the backend, use a specialized class to receive a JSON or CSV file of holidays, convert it, and save it as structured JSON.
                        Also, extend the functionality of the datetime library with a simple holiday check function, "is_holiday() -> bool". 
                        Receive more than one holiday calendar and select them from a list box (if possible).
            """),
            parent=self
        )

if __name__ == "__main__":
    # Example usage of TWindow
    try:       
        app = TWindow()
        app.mainloop()
    except KeyboardInterrupt as e:
        print("Encerrando a aplicação")
        exit(0) #? Aqui o código deve ser encerrado corretamente