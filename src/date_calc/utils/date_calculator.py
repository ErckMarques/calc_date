"""
This module provides a specialized class, for the purposes of this application,
that inherits(?)/encapsulates(?) functionality from datetime.datetime, the native library.
"""

from datetime import date, datetime, timedelta
from typing import TypeAlias, Literal

PositiveOrNegativeInt: TypeAlias = int

class DateCalculator:
    """
    A class to perform date calculations.
    """

    @staticmethod
    def add_days(start_date: datetime, days: PositiveOrNegativeInt) -> date:
        """
        Perform the calculation of the sum or difference between a given number and a number of days.

        Args:
            start_date (datetime): The starting date.
            days (int): The number of days to add.

        Returns:
            datetime: The new date after adding the days.
        """
        result = start_date + timedelta(days=days)
        return result.date()

    @staticmethod
    def date_difference(start_date: date, end_date: date) -> int:
        """
        Calculate the difference in days between two dates.

        Args:
            start_date (date): The starting date.
            end_date (date): The ending date.

        Returns:
            int: The number of days between the two dates.
        """
        return (end_date - start_date).days

    @staticmethod
    def days_until(date: date) -> int:
        """
        Calculate the number of days until a given date.

        Args:
            date (date): The target date.

        Returns:
            int: The number of days until the target date.
        """
        today = date.today()
        return (date - today).days
    
    @staticmethod
    def business_days(*, initial_date: date, final_date: date) -> int:
        """
        Calculate the number of business days until a given date.

        Args:
            date (date): The target date.

        Returns:
            int: The number of business days until the target date.
        """

        business_days = 0
        while initial_date < final_date:
            if initial_date.weekday() < 5:  # Monday to Friday are business days
                business_days += 1
            initial_date += timedelta(days=1)
        return business_days

    @staticmethod
    def consecutive_days(*, initial_date: date, final_date: date) -> int:
        """
        Calculate the number of consecutive days between two dates.

        Args:
            initial_date (date): The starting date.
            final_date (date): The ending date.

        Returns:
            int: The number of consecutive days between the two dates.
        """
        if initial_date > final_date:
            return 0
        return (final_date - initial_date).days
    
    @staticmethod
    def new_date_with_interval_of_days(
            *,
            initial_date: date,
            interval: PositiveOrNegativeInt,
            type_of_days: Literal["business", "consecutive"]
        ) -> date:
        """
        Calculate the date after adding a certain number of business days to an initial date.

        Args:
            initial_date (date): The starting date.
            interval (int): The number of business days to add.
            type_of_days (str): The type of days to consider ("business" or "consecutive").

        Returns:
            date: The new date after adding the business days.
        """
        current_date = initial_date
        days_added = 0
        step = 1 if interval > 0 else -1
        
        if type_of_days == "consecutive":
            return current_date + timedelta(days=interval)
        
        while days_added < abs(interval):
            if current_date.weekday() <= 5:  # Monday to Friday are business days
                days_added += 1
            current_date += timedelta(days=step)
            
            while current_date.weekday() >= 5:  # Skip weekends
                current_date += timedelta(days=step)
        return current_date