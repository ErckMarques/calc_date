from datetime import date
from typing import final
import ttkbootstrap as ttk
from ttkbootstrap.constants import INFO
from ttkbootstrap.tooltip import ToolTip
from PIL import Image, ImageTk

from date_calc.gui import find_image
from date_calc.gui.utils.grid_layout import ConfigureGridLayout
from date_calc.gui import TkContainer

@final
class FrameDateDifference(ttk.Labelframe, ConfigureGridLayout):
    """
    Labelframe for calculating the difference between two dates.

    Args:
        master (TkContainer): The parent widget.
        **kwargs: Additional keyword arguments.
    """

    def __init__(self, master: TkContainer, **kwargs) -> None:
        super().__init__(master, **kwargs)
        
        self._configure_label_frame()
        self._create_widgets()


    def _configure_label_frame(self) -> None:
        """
        Configure the label frame.
        """
        self.config(text="Date Difference", padding=(10, 10))
        

    def _create_widgets(self) -> None:
        """
        Create and place widgets in the frame.
        """
        self._create_date_entry_frame()
        self._create_label_response()
        self._create_buttons()

    def _create_date_entry_frame(self) -> None:
        """Create a frame for date entries with two 'ttk.DateEntry' widgets."""
        frame = ttk.Frame(self)
        self.configure_grid_layout(frame, rows=1, columns=2)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.start_date = ttk.DateEntry(frame, popup_title="Select Start Date")
        self.start_date.grid(row=0, column=0, padx=(2, 5), sticky="ew")
        ToolTip(self.start_date, "Select the start date", bootstyle="info")

        self.end_date = ttk.DateEntry(frame, popup_title="Select End Date")
        self.end_date.grid(row=0, column=1, padx=(0, 2), sticky="ew")
        ToolTip(self.end_date, "Select the end date", bootstyle="info")

    def _create_label_response(self) -> None:
        """Create a label to display the date difference response."""
        # Container
        frame = ttk.Frame(self)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        ttk.Label(frame, text="Difference:").pack(side="left", padx=(2, 0))

        self.result_var = ttk.StringVar(name="date_difference_response", value="0 days")
        ttk.Label(frame, textvariable=self.result_var).pack(side="left", padx=(5, 0))
        
        image_info = ImageTk.PhotoImage(Image.open(find_image("info")).resize((30, 30)))
        info = ttk.Label(frame, image=image_info, justify="center")
        ToolTip(
            info, 
            text="Allows you to calculate the difference between two dates", 
            bootstyle=INFO
        )
        setattr(info, "image", image_info)
        info.pack(side="right", padx=(0, 5))

    def _create_buttons(self) -> None:
        """Create buttons for calculating and resetting the date difference."""
        frame_buttons = ttk.Frame(self)
        self.configure_grid_layout(frame_buttons, rows=1, columns=2)
        frame_buttons.pack(padx=10, pady=10, fill="both", expand=True)

        calculate_button = ttk.Button(
            frame_buttons, text="Calculate",
            command=self._calculate_date_difference
        )
        calculate_button.grid(row=0, column=0, padx=(5, 0), sticky="ew")
        ToolTip(calculate_button, "Calculate the difference between the selected dates", bootstyle="info")

        reset_button = ttk.Button(frame_buttons, text="Reset", command=self._reset_date_entries)
        reset_button.grid(row=0, column=1, padx=(5, 0), sticky="ew")
        ToolTip(reset_button, "Clear the date entries", bootstyle="info")

    def _calculate_date_difference(self) -> None:
        start_date = self.start_date.get_date()
        end_date = self.end_date.get_date()
        if start_date and end_date:
            delta = end_date - start_date
            self.result_var.set(f"{delta.days} days")
            # colocar um relatório com dias úteis e finais de semana
        else:
            self.result_var.set("Invalid dates")

    def _reset_date_entries(self) -> None:
        self.start_date.set_date(date.today())
        self.end_date.set_date(date.today())
        self.result_var.set("0 days")
