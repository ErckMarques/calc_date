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

def test_consecutive_days():
    initial_date = datetime(2023, 1, 1).date()
    final_date = datetime(2023, 1, 10).date()
    result = DateCalculator.consecutive_days(initial_date=initial_date, final_date=final_date)
    assert result == 9  # 9 consecutive days between Jan 1 and Jan 10, 2023

def test_business_days_with_negative_interval():
    initial_date = datetime(2025, 9, 24).date()
    interval = -25  # 25 business days back, date should be 2025-08-20
    result = DateCalculator.new_date_with_interval_of_days(
        initial_date=initial_date,
        interval=interval,
        type_of_days="business"
    )
    assert result == datetime(2025, 8, 20).date()

def test_consecutive_days_with_negative_interval():
    initial_date = datetime(2025, 9, 24).date()
    interval = -25  # 25 consecutive days back, date should be 2025-08-30
    result = DateCalculator.new_date_with_interval_of_days(
        initial_date=initial_date,
        interval=interval,
        type_of_days="consecutive"
    )
    assert result == datetime(2025, 8, 30).date()