from collections.abc import Iterable
from datetime import datetime, timedelta
from pathlib import Path
from tkinter import Event
from typing import TypedDict

import ttkbootstrap as ttk

type TkContainer = ttk.Window | ttk.Frame | ttk.Labelframe

def create_gui() -> ttk.Window:
    root = ttk.Window(title="Date Calculator", themename="superhero")
    root.bind("<Escape>", lambda e: root.focus())

    _label_frame_date_difference(root)
    _label_frame_date_with_interval(root)

    return root

def _label_frame_date_difference(root: TkContainer) -> None:
    """
    Places a label frame at the root with two 'ttk.DateEntry' widgets and two buttons 
    to perform the actions of clearing fields and calculating day differences.
    """
    frame = ttk.Labelframe(root, text="Date Difference")
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    _date_entry_widgets(frame)

def _date_entry_widgets(root: TkContainer) -> None:
    """
    Adds two 'ttk.DateEntry' widgets, two buttons and a label for replies, to the given frame.
    """
    frame = ttk.Frame(root)
    frame.pack(padx=10, pady=10, expand=True)

    start_date = ttk.DateEntry(
        frame,
        popup_title="Select Start Date",
    )
    start_date.pack(side="left", padx=(2, 5))

    end_date = ttk.DateEntry(
        frame,
        popup_title="Select End Date",
    )
    end_date.pack(side="left", padx=(0, 2))

    result_var = _entry_date_response_label(root)
    
    _date_entry_buttons(root, start_date, end_date, result_var)

def _date_entry_buttons(frame: TkContainer, start_date: ttk.DateEntry, end_date: ttk.DateEntry, result_var: ttk.StringVar) -> None:
    """
    Adds 'Calculate' and 'Clear' buttons to the given frame.
    """
    f = ttk.Frame(frame)
    f.pack(pady=10)
    calculate_button = ttk.Button(
        f, text="Calculate",
        command=lambda: _calculate_date_difference(
            start_date.get_date(), end_date.get_date(), result_var
        )
    )
    calculate_button.pack(side="left", padx=(5, 0))

    clear_button = ttk.Button(f, text="Clear", command=lambda: _clear_date_entries(start_date, end_date))
    clear_button.pack(side="left", padx=(5, 0))

def _entry_date_response_label(root: TkContainer) -> ttk.StringVar:
    """
    Adds labels to the given frame to display the results.
    """
    frame = ttk.Frame(root)
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    ttk.Label(frame, text="Difference from:").pack(side="left", padx=(5, 0))
    date_difference_response = ttk.StringVar(name="date_difference_response", value="0 days")
    result_label = ttk.Label(frame, textvariable=date_difference_response)
    result_label.pack(side="left", padx=(5, 0))

    return date_difference_response

def _label_frame_date_with_interval(root: TkContainer) -> None:
    """
    Places a label frame at the root with a 'ttk.DateEntry' widget and a button 
    to perform the action of calculating a new date with an interval.
    """
    frame = ttk.Labelframe(root, text="Date with Interval")
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    _date_with_interval_widgets(frame)

def _calculate_date_difference(start_date: datetime, end_date: datetime, result_var: ttk.StringVar) -> None:
    """
    Calculates the difference in days between two dates and updates the result label.
    """
    if start_date and end_date:
        delta: timedelta = end_date - start_date
        result_var.set(f"{delta.days} days")
    else:
        result_var.set("Invalid dates")

def _clear_date_entries(start_date: ttk.DateEntry, end_date: ttk.DateEntry) -> None:
    """
    Clears the date entry fields.
    """
    start_date.set_date(datetime.now().date().replace(day=1))
    end_date.set_date(datetime.now().date().replace(day=1))

def _date_with_interval_widgets(root: TkContainer) -> None:
    """
    Adds a 'ttk.DateEntry' widget, an interval entry, and a button to the given frame.
    """
    frame = ttk.Frame(root)
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    date_entry = ttk.DateEntry(
        frame,
        popup_title="Select Date",
    )
    date_entry.pack(side="left", padx=(2, 5))

    input_var = ttk.StringVar(name="date_with_interval_input", value="0")
    interval_entry = ttk.Entry(frame, textvariable=input_var)
    # possibilidade de selecionar tudo usando CTRL+A/a
    interval_entry.bind("<Control-A>", lambda e: interval_entry.selection_range(0, ttk.END))
    interval_entry.bind("<Control-a>", lambda e: interval_entry.selection_range(0, ttk.END))
    # validação de entrada numérica
    interval_entry.bind("<KeyPress>", _add_numeric_validation)
    # realiza o calculo da data ao pressionar a tecla enter, com foco no campo de entrada
    interval_entry.bind("<Return>", 
        lambda e: _calculate_date_with_interval(
            date_entry.get_date(), 
            int(input_var.get()), 
            result_var
        )
    )
    interval_entry.pack(side="left", padx=(0, 5))

    result_var = _date_with_interval_response_label(root)

    _date_with_interval_buttons(frame, date_entry, input_var, result_var)

def _date_with_interval_response_label(root: TkContainer) -> ttk.StringVar:
    frame = ttk.Frame(root)
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    ttk.Label(frame, text="New date:").pack(side="left", padx=(5, 0))
    date_with_interval_response = ttk.StringVar(
        name="date_with_interval_response",
        value=f"{datetime.now().strftime('%A, %d de %B de %Y').capitalize()}"
    )
    result_label = ttk.Label(frame, textvariable=date_with_interval_response)
    result_label.pack(side="left", padx=(5, 0))

    return date_with_interval_response

def _date_with_interval_buttons(
        frame: TkContainer, 
        date_entry: ttk.DateEntry,
        input_var: ttk.StringVar,
        result_var: ttk.StringVar
        ) -> None:
    """
    Adds buttons to the given frame to calculate a new date with an interval.
    """
    try:
        calculate_button = ttk.Button(
            frame, text="Calculate",
            command=lambda: _calculate_date_with_interval(
                date_entry.get_date(), int(input_var.get()), result_var
            )
        )
        calculate_button.pack(side="left", padx=(5, 0))
    except ValueError:
        input_var.set("invalid input".capitalize())  # Reset to default if conversion fails

def _calculate_date_with_interval(date: datetime, interval: int, result_var: ttk.StringVar) -> None:
    """Calculates a new date by adding an interval in days to the given date and updates the result label."""
    if date and interval:
            new_date = date + timedelta(days=interval)
            result_var.set(new_date.strftime('%A, %d de %B de %Y').capitalize())
    elif interval == 0:
        result_var.set(date.strftime('%A, %d de %B de %Y').capitalize())
    else:
        result_var.set("Invalid date or interval")

def _add_numeric_validation(e: Event) -> None:
    """
    Validates that the input is numeric. If not, it prevents the event.
    """
    if e.char and not e.char.isdigit() and e.char not in ('\b', '\x7f', '-'):
        e.widget.bell()  # Optional: make a sound to indicate invalid input
        return "break"  # Prevent the event from propagating
    return None

def main() -> None:
    """
    Main function to create and run the GUI application.
    """
    import locale
    import sys

    if sys.platform.startswith('win'):
        # Configura para português do Brasil no Windows
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    else:
        # Configura para português do Brasil em outros sistemas
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

    app = create_gui()
    app.mainloop()

if __name__ == "__main__":
    main()