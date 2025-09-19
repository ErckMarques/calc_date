from datetime import datetime, timedelta

class DefaultRunner:

    def sum(self, date: datetime, days: timedelta) -> str:
        result = date + days
        return result.strftime('%d-%m-%Y -> %A')

    def diff(self, start: datetime, end: datetime) -> str:
        result = end - start
        if result.days < 0:
            return "Start date must be before end date."
        elif result.days == 0:
            return "The dates are the same."
        else:
            return str(result.days)
    
    def enter_interactive_mode(self) -> None:
        print("Mode under development.")
    
    def compile_translations(self, path: str) -> None:
        from date_calc.translate.compile import compile_po_2_mo
        
        compile_po_2_mo(path)