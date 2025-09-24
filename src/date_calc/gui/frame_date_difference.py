from datetime import date, timedelta
from typing import final
import ttkbootstrap as ttk
from ttkbootstrap.constants import INFO
from ttkbootstrap.tooltip import ToolTip

from date_calc import TkContainer, ICON_PATH, t
from date_calc.gui.utils.grid_layout import ConfigureGridLayout
from date_calc.utils.date_calculator import DateCalculator

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
        self.config(text=t("Dates Difference"), padding=(10, 10))
        

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
        self.configure_grid_layout(frame, rows=1, columns=3)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.start_date = ttk.DateEntry(frame, popup_title="Select Start Date", startdate=date.today().replace(day=1))
        # self.start_date.entry.bind("<KeyPress>", self._on_key_press)
        self.start_date.grid(row=0, column=0, padx=(2, 5), sticky="ew")
        ToolTip(self.start_date, t("Select the start date"), bootstyle="info")

        self.end_date = ttk.DateEntry(frame, popup_title="Select End Date", startdate=date.today())
        self.end_date.grid(row=0, column=1, padx=(0, 2), sticky="ew")
        ToolTip(self.end_date, t("Select the end date"), bootstyle="info")

    def _create_label_response(self) -> None:
        """Create a label to display the date difference response."""
        # Container
        frame = ttk.Frame(self)
        self.configure_grid_layout(frame, rows=1, columns=3)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        # ttk.Label(frame, text="Difference:").grid(row=0, column=0, padx=(5, 0), sticky="w")

        self.result_var = ttk.StringVar(name="date_difference_response", value=f"{t("Difference:")}  0 {t("days")}")
        ttk.Label(frame, textvariable=self.result_var).grid(row=0, column=0, padx=(5, 0), sticky="w")

        self.business_days_var = ttk.StringVar(name="business_days_response", value=f"{t("Business Days:")}  0 {t("days")}")
        ttk.Label(frame, textvariable=self.business_days_var).grid(row=0, column=1, padx=(5, 0), sticky="w")

        image_info = ttk.PhotoImage(name="info_icon", file=ICON_PATH.joinpath("info.png")).subsample(25)
        info = ttk.Label(frame, image=image_info)
        info.grid(row=0, column=2, padx=(2, 0), sticky="e")
        setattr(info, "_image_info", image_info)  # Prevent garbage collection
        ToolTip(
            info, 
            text=t("Allows you to calculate the difference between two dates"), 
            bootstyle=INFO
        )

    def _create_buttons(self) -> None:
        """Create buttons for calculating and resetting the date difference."""
        frame_buttons = ttk.Frame(self)
        self.configure_grid_layout(frame_buttons, rows=1, columns=2)
        frame_buttons.pack(padx=10, pady=10, fill="both", expand=True)

        calculate_button = ttk.Button(
            frame_buttons, text=t("Calculate"),
            command=self._calculate_date_difference
        )
        calculate_button.grid(row=0, column=0, padx=(5, 0), sticky="ew")
        ToolTip(calculate_button, t("Calculates the number of days between selected dates"), bootstyle="info")

        reset_button = ttk.Button(frame_buttons, text=t("Clear"), command=self._reset_date_entries)
        reset_button.grid(row=0, column=1, padx=(5, 0), sticky="ew")
        ToolTip(reset_button, t("Clears the answer fields and resets the date input fields"), bootstyle="info")

    def _calculate_date_difference(self) -> None:
        start_date = self.start_date.get_date()
        end_date = self.end_date.get_date()
        if start_date and end_date:
            consec_days = DateCalculator.date_difference(start_date, end_date)
            business_days = DateCalculator.business_days(initial_date=start_date, final_date=end_date)
            
            self.result_var.set(f"{t("Difference:")}  {consec_days} {t("days")}") 
            self.business_days_var.set(f"{t("Business Days:")}  {business_days} {t("days")}")
        else:
            self.result_var.set("Invalid dates")

    def _reset_date_entries(self) -> None:
        self.start_date.set_date(date.today().replace(day=1))
        self.end_date.set_date(date.today())
        self.result_var.set(f"{t("Difference:")}  0 {t("days")}")
