from __future__ import annotations
from datetime import date, timedelta
from tkinter import Misc
from typing import Callable, Literal, final, TypeAlias
import ttkbootstrap as ttk
from ttkbootstrap.tooltip import ToolTip

from frame_date_difference import ConfigureGridLayout

TKContainer: TypeAlias = ttk.Window | ttk.Frame | ttk.Labelframe

@final
class FrameDateWithInterval(ttk.Labelframe, ConfigureGridLayout):
    def __init__(self, 
        master: Misc | None = None, 
        **kwargs
    ) -> None:
        super().__init__(
            master, 
            **kwargs
        )
        self._configure_label_frame()
        self._create_widgets()

    def _configure_label_frame(self) -> None:
        self.configure(text="Date with Interval", padding=(10, 5))

    def _create_widgets(self) -> None:
        self._create_date_with_interval_widgets()
        self._create_label_response()

    def _create_date_with_interval_widgets(self) -> None:
        frame = ttk.Frame(self)
        self.configure_grid_layout(frame, rows=1, columns=3)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.start_date = ttk.DateEntry(frame, popup_title="Select Start Date")
        self.start_date.grid(row=0, column=0, padx=(2, 5), sticky="ew")

        self.days = ttk.IntVar(name="input_days")
        ttk.Entry(frame, textvariable=self.days).grid(row=0, column=1, padx=(0, 5), sticky="ew")

        ttk.Button(frame, text="Calculate", command=self._calculate).grid(row=0, column=2, padx=(0, 2), sticky="ew")

    def _create_label_response(self) -> None:
        frame = ttk.Frame(self)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        ttk.Label(frame, text="Result:").pack(side="left", padx=(2, 0))

        self.result_var = ttk.StringVar(name="date_with_interval_response", value=date.today().strftime("%A, %d de %B de %Y").capitalize())
        ttk.Label(frame, textvariable=self.result_var).pack(side="left", padx=(5, 0))

    def _calculate(self) -> None:
        start_date = self.start_date.get_date()
        days = self.days.get()
        if start_date and days:
            new_date = start_date + timedelta(days=days)
            self.result_var.set(new_date.strftime("%A, %d de %B de %Y").capitalize())
        else:
            self.result_var.set("Invalid input")
