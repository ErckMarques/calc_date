from tkinter import Frame
from datetime import date
from dateutil.parser import parse as dateparse
from tkinter import StringVar
import ttkbootstrap as ttk
from ttkbootstrap.widgets import DateEntry


class DateVar(StringVar):
    """A specialized Tkinter variable for date handling.
    
    Extends StringVar to work with Python date objects, providing automatic
    conversion between strings and date objects, with support for multiple
    date formats and change notifications.
    
    Attributes:
        formats (list[str]): List of accepted date formats.
        on_change (callable): Callback function triggered when value changes.
    """

    def __init__(self, *args, formats=None, on_change=None, **kwargs):
        """Initializes the DateVar.
        
        Args:
            *args: Positional arguments for StringVar.
            formats (list[str], optional): Accepted date formats. Defaults to
                ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"].
            on_change (callable, optional): Function called when value changes.
            **kwargs: Keyword arguments for StringVar.
        """
        super().__init__(*args, **kwargs)
        self.formats = formats or ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]
        self.on_change = on_change
        self.trace_add("write", self._on_write)

    def get_date(self) -> date | None:
        """Gets the current value as a date object.
        
        Returns:
            date | None: The date object corresponding to current value or None
                if the value cannot be converted to a valid date.
        """
        try:
            return dateparse(self.get(), dayfirst=True).date()
        except Exception:
            return None

    def set_date(self, value: date):
        """Sets the value using a date object.
        
        Args:
            value (date): The date object to set as value.
        """
        self.set(value.isoformat())

    def _on_write(self, *args):
        """Internal callback triggered when the variable value changes.
        
        Calls the on_change function if defined, passing the current value as date.
        """
        if self.on_change:
            self.on_change(self.get_date())


class DateField(Frame):
    """Custom widget for date input with validation.
    
    Combines a Label with ttkbootstrap's DateEntry, providing visual
    validation and simplified date handling.
    
    Attributes:
        var (DateVar): The variable storing the date value.
        label (ttk.Label): The field label.
        entry (DateEntry): The date entry widget.
        _external_callback (callable): External callback for value changes.
    """

    def __init__(self, master, label="Date", on_change=None, default=None, bootstyle="info", **kwargs):
        """Initializes the DateField.
        
        Args:
            master: Parent widget.
            label (str, optional): Label text. Defaults to "Date".
            on_change (callable, optional): Function called when date changes.
            default (date, optional): Initial default value.
            bootstyle (str, optional): ttkbootstrap visual style. Defaults to "info".
            **kwargs: Additional arguments for Frame.
        """
        super().__init__(master, **kwargs)
        self.var = DateVar(on_change=self._on_change)
        self.label = ttk.Label(self, text=label)
        self.entry = DateEntry(self, textvariable=self.var, bootstyle=bootstyle)
        self.label.pack(side="left", padx=5)
        self.entry.pack(side="left", padx=5)
        self._external_callback = on_change

        if default:
            self.var.set_date(default)

    def _on_change(self, value):
        """Internal callback for date value changes.
        
        Updates the field appearance based on date validity and calls
        the external callback if defined.
        
        Args:
            value (date | None): The new date value.
        """
        # Visual validation
        if value:
            self.entry.configure(bootstyle="success")
        else:
            self.entry.configure(bootstyle="danger")
        # External callback
        if self._external_callback:
            self._external_callback(value)

    def get_date(self):
        """Gets the current date from the field.
        
        Returns:
            date | None: The current date object or None if invalid.
        """
        return self.var.get_date()

    def set_date(self, value: date):
        """Sets the field's date.
        
        Args:
            value (date): The date object to set.
        """
        self.var.set_date(value)