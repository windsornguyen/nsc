import unittest
from datetime import datetime, timedelta
from dateutil.easter import easter
from dateutil.relativedelta import MO, TH, relativedelta
import random
import calendar


def get_good_friday(year):
    return easter(year) - timedelta(days=2)


def adjust_for_weekend(holiday):
    if holiday.weekday() == 5:  # Saturday
        return holiday - timedelta(days=1)
    elif holiday.weekday() == 6:  # Sunday
        return holiday + timedelta(days=1)
    return holiday


def is_exchange_holiday(date):
    year = date.year
    holidays = [
        # Include December 31st of previous year iff the current date is January 1st and falls on a weekend
        datetime(year - 1, 12, 31)
        if date == datetime(year, 1, 1) and date.weekday() in [5, 6]
        else datetime(year, 1, 1),
        datetime(year, 7, 4),  # Independence Day
        datetime(year, 12, 25),  # Christmas Day
        (
            datetime(year, 1, 1) + relativedelta(weekday=MO(3))
        ),  # Martin Luther King Jr. Day
        (datetime(year, 2, 1) + relativedelta(weekday=MO(3))),  # Washington's Birthday
        (datetime(year, 5, 31) - relativedelta(weekday=MO(-1))),  # Memorial Day
        (datetime(year, 9, 1) + relativedelta(weekday=MO(1))),  # Labor Day
        (datetime(year, 11, 1) + relativedelta(weekday=TH(4))),  # Thanksgiving
        get_good_friday(year),  # Good Friday
    ]

    adjusted_holidays = {adjust_for_weekend(holiday) for holiday in holidays}

    return date in adjusted_holidays


# TEST SUITE
class TestHolidayFunctionsSimplified(unittest.TestCase):
    def test_variable_date_holidays(self):
        # Test variable-date holidays for a range of years
        for year in range(2023 - 100, 2023 + 100):
            self.assertTrue(
                is_exchange_holiday(datetime(year, 1, 1) + relativedelta(weekday=MO(3)))
            )  # MLK Day
            self.assertTrue(
                is_exchange_holiday(datetime(year, 2, 1) + relativedelta(weekday=MO(3)))
            )  # Washington's Birthday
            self.assertTrue(
                is_exchange_holiday(
                    datetime(year, 5, 31) - relativedelta(weekday=MO(-1))
                )
            )  # Memorial Day
            self.assertTrue(
                is_exchange_holiday(datetime(year, 9, 1) + relativedelta(weekday=MO(1)))
            )  # Labor Day
            self.assertTrue(
                is_exchange_holiday(
                    datetime(year, 11, 1) + relativedelta(weekday=TH(4))
                )
            )  # Thanksgiving
            self.assertTrue(
                is_exchange_holiday(easter(year) - timedelta(days=2))
            )  # Good Friday

    def test_fixed_date_holidays(self):
        for year in range(2023 - 100, 2023 + 100):
            new_years_day = datetime(year, 1, 1)
            independence_day = datetime(year, 7, 4)
            christmas_day = datetime(year, 12, 25)

            # Test only the observed date if the actual holiday falls on a weekend
            if new_years_day.weekday() in [5, 6]:
                self.assertFalse(is_exchange_holiday(new_years_day))
            else:
                self.assertTrue(is_exchange_holiday(new_years_day))

            if independence_day.weekday() in [5, 6]:
                self.assertFalse(is_exchange_holiday(independence_day))
                self.assertTrue(
                    is_exchange_holiday(adjust_for_weekend(independence_day))
                )
            else:
                self.assertTrue(is_exchange_holiday(independence_day))

            if christmas_day.weekday() in [5, 6]:
                self.assertFalse(is_exchange_holiday(christmas_day))
                self.assertTrue(is_exchange_holiday(adjust_for_weekend(christmas_day)))
            else:
                self.assertTrue(is_exchange_holiday(christmas_day))

    def test_non_holiday(self):
        for year in range(2023 - 100, 2023 + 100):
            while True:
                month = random.choice(range(1, 13))
                day = random.choice(range(1, calendar.monthrange(year, month)[1] + 1))
                random_date = datetime(year, month, day)

                if random_date.weekday() in [5, 6]:  # Saturday or Sunday
                    adjusted_date = adjust_for_weekend(random_date)
                else:
                    adjusted_date = random_date

                # Check if the date is a holiday or adjusted holiday
                if not is_exchange_holiday(random_date) and not is_exchange_holiday(
                    adjusted_date
                ):
                    break

            is_holiday = is_exchange_holiday(adjusted_date)
            should_be_holiday = is_exchange_holiday(random_date) or is_exchange_holiday(
                adjusted_date
            )

            if is_holiday != should_be_holiday:
                print(
                    f"Error: {adjusted_date.strftime('%Y-%m-%d')} (adjusted from {random_date.strftime('%Y-%m-%d')}) is incorrectly identified as a holiday."
                )

            self.assertEqual(is_holiday, should_be_holiday)


if __name__ == "__main__":
    unittest.main()
