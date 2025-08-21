from datetime import date
from typing import final
import ttkbootstrap as ttk
from ttkbootstrap.tooltip import ToolTip

type TkContainer = ttk.Window | ttk.Frame | ttk.Labelframe

class ConfigureGridLayout:
    @staticmethod
    def configure_grid_layout(container: TkContainer, *, rows: int, columns: int) -> None:
        """
        Configure the grid layout for the given container.
        """
        for col in range(columns):
            container.grid_columnconfigure(col, weight=1)
        for row in range(rows):
            container.grid_rowconfigure(row, weight=1)

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
        frame_dtentry = ttk.Frame(self)
        self.configure_grid_layout(frame_dtentry, rows=1, columns=2)
        frame_dtentry.pack(padx=10, pady=10, fill="both", expand=True)

        self.start_date = ttk.DateEntry(frame_dtentry, popup_title="Select Start Date")
        self.start_date.grid(row=0, column=0, padx=(2, 5), sticky="ew")
        ToolTip(self.start_date, "Select the start date", bootstyle="info")

        self.end_date = ttk.DateEntry(frame_dtentry, popup_title="Select End Date")
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
        else:
            self.result_var.set("Invalid dates")

    def _reset_date_entries(self) -> None:
        self.start_date.set_date(date.today())
        self.end_date.set_date(date.today())
        self.result_var.set("0 days")
