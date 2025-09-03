from textwrap import dedent
from ttkbootstrap.dialogs import Messagebox

devolpment = Messagebox.show_info(
    message=dedent(
        """
        Em desenvolvimento
        """
    ),
    title="resource under development"
)