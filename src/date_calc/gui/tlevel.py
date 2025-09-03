from typing import final
from ttkbootstrap import Toplevel

from date_calc import ICON_PATH
from date_calc.gui.frame_date_difference import ConfigureGridLayout

@final
class CustomToplevel(Toplevel, ConfigureGridLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._configure_custom_top_level()
        self._add_form()

    def _configure_custom_top_level(self) -> None:
        # self.resizable(False, False)
        self.bind("<Escape>", lambda e: self.focus_set())
        self.title("Configuration")
        self.iconbitmap(ICON_PATH.joinpath("dev.ico"))

    def _add_form(self) -> None: pass

if __name__ == "__main__":
    app = CustomToplevel()
    app.mainloop()