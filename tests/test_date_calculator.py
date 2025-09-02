from datetime import datetime

from date_calc.utils.date_calculator import DateCalculator

def test_add_days():
    start_date = datetime(2023, 1, 1)
    days_to_add = 5
    result = DateCalculator.add_days(start_date, days_to_add)
    assert result == datetime(2023, 1, 6).date()

def test_business_days():
    initial_date = datetime(2023, 1, 1).date()
    final_date = datetime(2023, 1, 10).date()
    result = DateCalculator.business_days(initial_date=initial_date, final_date=final_date)
    assert result == 6  # 6 business days between Jan 1 and Jan 10, 2023