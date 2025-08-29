from date_calc import TkContainer

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