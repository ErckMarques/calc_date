from __future__ import annotations
from datetime import date, timedelta
from tkinter import Misc, Event
from typing import final

from PIL import Image, ImageDraw, ImageTk
import ttkbootstrap as ttk
from ttkbootstrap.tooltip import ToolTip
from ttkbootstrap.constants import INFO, DANGER, PRIMARY

from date_calc import TkContainer, ICON_PATH, t
from date_calc.gui.frame_date_difference import ConfigureGridLayout

@final
class FrameDateWithInterval(ttk.Labelframe, ConfigureGridLayout):
    def __init__(self, 
        master: TkContainer, 
        **kwargs
    ) -> None:
        super().__init__(
            master, 
            **kwargs
        )
        self._configure_label_frame()
        self._create_widgets()

    def _configure_label_frame(self) -> None:
        self.configure(text=t("Day Counter and Date Calculator"), padding=(10, 5))

    def _create_widgets(self) -> None:
        """Create and arrange widgets in the frame."""
        self._create_date_with_interval_widgets()
        self._create_frame_radio()
        self._create_label_response()

    def _create_date_with_interval_widgets(self) -> None:
        frame = ttk.Frame(self)
        self.configure_grid_layout(frame, rows=1, columns=3)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.start_date = ttk.DateEntry(
            frame,
            popup_title="Select Start Date",
            startdate=date.today().replace(day=1)
        )
        self.start_date.grid(row=0, column=0, padx=(2, 5), sticky="ew")
        ToolTip(self.start_date, text=t("Select Start Date"), bootstyle=INFO)

        self.days = ttk.IntVar(name="input_days")
        entry = ttk.Entry(frame, textvariable=self.days)
        entry.bind("<FocusIn>", self._entry_event_in)
        entry.bind("<KeyPress>", self._entry_event_out)
        entry.bind("<Control-A>", lambda e: entry.selection_range(0, ttk.END))
        entry.bind("<Control-a>", lambda e: entry.selection_range(0, ttk.END))
        entry.bind("<Escape>", lambda e: self.winfo_toplevel().focus_set())
        entry.grid(row=0, column=1, padx=(0, 5), sticky="ew")
        ToolTip(entry, text=t("Enter a positive or negative number of days"), bootstyle=INFO)

        btn = ttk.Button(frame, text=t("Calculate"), command=self._calculate)
        btn.grid(row=0, column=2, padx=(0, 2), sticky="ew")
        ToolTip(btn, text=t("Calculates the new date"), bootstyle=INFO)

    def _create_frame_radio(self) -> None:
        frame = ttk.Frame(self)
        self.configure_grid_layout(frame, rows=1, columns=3)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        # fix this
        self.interval_type = ttk.StringVar(value="days")
        r = ttk.Radiobutton(
            frame, text=t("Consecutive Days"),
            variable=self.interval_type, value="consecutive"
        )
        r.grid(row=0, column=0, padx=(2, 0), sticky="w")
        ToolTip(r, t("If checked, performs the calculation for the new date with calendar days"), bootstyle=INFO)

        r = ttk.Radiobutton(
            frame, text=t("Business Days"),
            variable=self.interval_type, value="business"
        )
        r.grid(row=0, column=1, padx=(2, 0), sticky="w")
        ToolTip(r, t("If checked, perform the calculation for the new date with working days"), bootstyle=INFO)

        image_info = ttk.PhotoImage(name="info_icon", file=ICON_PATH.joinpath("info.png")).subsample(25)
        info = ttk.Label(frame, image=image_info)
        info.grid(row=0, column=2, padx=(2, 0), sticky="e")
        setattr(info, "_image_info", image_info)  # Prevent garbage collection
        ToolTip(
            info, 
            text=t("Allows you to calculate a date from a number of calendar days or business days"), 
            bootstyle=INFO
        )

    def _create_label_response(self) -> None:
        frame = ttk.Frame(self)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        ttk.Label(frame, text=t("Result")).pack(side="left", padx=(2, 0))

        self.result_var = ttk.StringVar(
            name="date_with_interval_response", 
            value=date.today().replace(day=1).strftime("%A, %d de %B de %Y").capitalize()
        )
        ttk.Label(frame, textvariable=self.result_var).pack(side="left", padx=(5, 0))

    def _entry_event_in(self, e: Event) -> None:
        if isinstance(e.widget, ttk.Entry):
            e.widget.delete(0, ttk.END)

    def _entry_event_out(self, e: Event) -> None:
        if e.char and not e.char.isdigit() and e.char not in ('\b', '\x7f', '-'):
            e.widget.bell()  # Optional: make a sound to indicate invalid input
            e.widget.configure(bootstyle=DANGER)
            return "break"  # Prevent the event from propagating
        else:
            e.widget.configure(bootstyle=PRIMARY)
        return None

    def _calculate(self) -> None:
        """Calculate the new date based on the input days and interval type."""
        # Get the start date and number of days from the user input
        start_date = self.start_date.get_date()
        days = self.days.get()
        # checks if there is any entry
        if start_date and days:
            # check if the interval type is business
            if self.interval_type.get() == "business":
                current_date = start_date
                added_days: int = 0  # control variable
                # calculate the new date manually
                while added_days < days:
                    current_date += timedelta(days=1)
                    # check if the current date is a weekday
                    if current_date.weekday() < 5:
                        added_days += 1
                new_date = current_date
            else:
                new_date = start_date + timedelta(days=days)
            self.result_var.set(new_date.strftime("%A, %d de %B de %Y").capitalize())
        else:
            self.result_var.set(t("Invalid Input"))
