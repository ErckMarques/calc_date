"""
This file provides a TWindow class, which inherits from ttkbootstrap.Window, marked with the typing.final decorator.
This TWindow holds all the logic related to the application's main window.
"""

from typing import final
from pathlib import Path

import sys
import pystray
from PIL import Image
from ttkbootstrap import Window, PhotoImage

ICON_PATH: Path = Path(__file__).parents[2].joinpath("assets", "date_calc.png")


@final
class TWindow(Window):
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
        self._configure_py_stray()
        # Add widgets
        # self._add_widgets()

    def _configuration_of_window(self) -> None:
        """
        Configure the window settings.
        """
        self.resizable(False, False)
        self.bind("<Control-BackSpace>", lambda e: self.destroy())
        self.bind("<Escape>", lambda e: self.focus_set())
        if sys.platform == "win32":
            self.iconbitmap(ICON_PATH.parent.joinpath("date_calc.ico"))
        else:
            # Linux and macOS
            self.iconphoto(True, PhotoImage(file=ICON_PATH))


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

    def _configure_grid_layout(self) -> None:
        """
        Configure the grid layout for the main window.
        """
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def _add_widgets(self) -> None:
        """
        Add widgets to the main window.
        """
        # Configure grid layout for widgets
        self._configure_grid_layout()


if __name__ == "__main__":
    # Example usage of TWindow
    try:
        from frame_date_difference import FrameDateDifference
        from frame_data_interval import FrameDateWithInterval
        
        window = TWindow(title="Date Calculator", themename="darkly")
        FrameDateDifference(window).pack(pady=10, padx=10, fill="both", expand=True)
        FrameDateWithInterval(window).pack(pady=10, padx=10, fill="both", expand=True)
        window.mainloop()
    except KeyboardInterrupt as e:
        print("Encerrando a aplicação")
        exit(0) #? Aqui o código deve ser encerrado corretamente
