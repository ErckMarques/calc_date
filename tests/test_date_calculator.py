import pytest
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

@pytest.mark.parametrize(
    "initial_date,interval,expected_date",
    [
        (datetime(2025, 10, 1).date(), -3, datetime(2025, 9, 26).date()),  # Wednesday -3 business days = previous Friday
        (datetime(2025, 10, 10).date(), 1, datetime(2025, 10, 13).date()),  # Friday +1 business day = next Monday
        (datetime(2025, 10, 6).date(), 25, datetime(2025, 11, 10).date()) # Monday +25 busines day = Monday, 10/11/2025
    ]
)
def test_new_date_with_business_days_negative_interval(initial_date, interval, expected_date):
    result = DateCalculator.new_date_with_interval_of_days(
        initial_date=initial_date,
        interval=interval,
        type_of_days="business"
    )
    assert result == expected_date
